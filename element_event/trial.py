"""Events are linked to Trials"""

import datajoint as dj
import inspect
import importlib
from . import event


schema = dj.schema()

_linking_module = None


def activate(
    trial_schema_name,
    event_schema_name,
    *,
    create_schema=True,
    create_tables=True,
    linking_module=None,
):
    """
    activate(trial_schema_name, event_schema_name, *, create_schema=True,
             create_tables=True, linking_module=None)
        :param trial_schema_name: schema name on the database server to activate
                            the `trial` element
        :param event_schema_name: schema name on the database server to activate
                            the `event` element
        :param create_schema: when True (default), create schema in the
                              database if it does not yet exist.
        :param create_tables: when True (default), create tables in the
                              database if they do not yet exist.
        :param linking_module: a module (or name) containing the required
                               dependencies to activate the `trial` element:
        Upstream tables:
            + Session: parent table to BehaviorRecording, typically
                       identifying a recording session.
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'dependency' must" + " be a module or module name"
    )

    global _linking_module
    _linking_module = linking_module

    event.activate(
        event_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        linking_module=_linking_module,
    )

    schema.activate(
        trial_schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=_linking_module.__dict__,
    )


# ----------------------------- Table declarations ----------------------


@schema
class Block(dj.Imported):
    definition = """ # Experimental blocks
    -> event.BehaviorRecording
    block_id               : smallint # block number (1-based indexing)
    ---
    block_start_time       : float     # (s) relative to recording start
    block_stop_time        : float     # (s) relative to recording start
    """

    class Attribute(dj.Part):
        definition = """  # Additional block attributes to fully describe a block
        -> master
        attribute_name    : varchar(16)
        ---
        attribute_value   : varchar(2000)
        """

    def make(self, key):
        raise NotImplementedError("For `insert`, use `allow_direct_insert=True`")


@schema
class TrialType(dj.Lookup):
    definition = """
    trial_type                : varchar(16)
    ---
    trial_type_description='' : varchar(256)
    """


@schema
class Trial(dj.Imported):
    definition = """  # Experimental trials
    -> event.BehaviorRecording
    trial_id            : smallint # trial number (1-based indexing)
    ---
    -> TrialType
    trial_start_time    : float  # (second) relative to recording start
    trial_stop_time     : float  # (second) relative to recording start
    """

    class Attribute(dj.Part):
        definition = """  # Additional trial attributes to fully describe a trial
        -> master
        attribute_name  : varchar(16)
        ---
        attribute_value : varchar(2000)
        """

    def make(self, key):
        raise NotImplementedError("For `insert`, use `allow_direct_insert=True`")


@schema
class BlockTrial(dj.Imported):
    definition = """
    -> Block
    -> Trial
    """    
    
    def make(self, key):
        raise NotImplementedError("For `insert`, use `allow_direct_insert=True`")


@schema
class TrialEvent(dj.Imported):
    definition = """
    -> Trial
    -> event.Event
    """

    def make(self, key):
        raise NotImplementedError("For `insert`, use `allow_direct_insert=True`")


# ---- HELPER ----


def get_trialized_alignment_event_times(alignment_event_key, trial_restriction):
    """
    For the trials identified by trial_restriction, identify recording times with 
        with respect to a given alignment_event. 
    :param alignment_event_key: key including information from event.AlignmentEvent
    :param trial_restriction: set or subset of trials from trial.Trial
    
    returns pandas dataframe with each of the following
        trial_key: key identifying a single trial
        start: recording time (s) of the beginning of an alignment window
        event: recording time (s) of an alignment event within the trial. 
               If multiple events within a trial, select the last one.
        end:  recording time (s) of the end of an alignment window
    """

    import pandas as pd

    session_key = (_linking_module.Session & trial_restriction).fetch1("KEY")
    trial_keys, trial_starts, trial_ends = (Trial ^ trial_restriction).fetch(
        "KEY", "trial_start_time", "trial_stop_time", order_by="trial_id"
    )
    alignment_spec = (event.AlignmentEvent & alignment_event_key).fetch1()

    alignment_times = []
    for trial_key, trial_start, trial_stop in zip(trial_keys, trial_starts, trial_ends):
        alignment_event_time = (
            event.Event
            & session_key
            & {"event_type": alignment_spec["alignment_event_type"]}
            & f"event_start_time BETWEEN {trial_start} AND {trial_stop}"
        )
        if alignment_event_time:
            # if  multiple alignment events, pick the last one in the trial
            alignment_event_time = alignment_event_time.fetch(
                "event_start_time", order_by="event_start_time DESC", limit=1
            )[0]
        else:
            alignment_times.append(
                {"trial_key": trial_key, "start": None, "event": None, "end": None}
            )
            continue

        alignment_start_time = (
            event.Event
            & session_key
            & {"event_type": alignment_spec["start_event_type"]}
            & f"event_start_time < {alignment_event_time}"
        )
        if alignment_start_time:
            # if multiple start events, pick most immediate prior alignment event
            alignment_start_time = alignment_start_time.fetch(
                "event_start_time", order_by="event_start_time DESC", limit=1
            )[0]
            alignment_start_time = max(alignment_start_time, trial_start)
        else:
            alignment_start_time = trial_start

        alignment_end_time = (
            event.Event
            & session_key
            & {"event_type": alignment_spec["end_event_type"]}
            & f"event_start_time > {alignment_event_time}"
        )
        if alignment_end_time:
            # if multiple of such start event, pick most immediate after alignment event
            alignment_end_time = alignment_end_time.fetch(
                "event_start_time", order_by="event_start_time", limit=1
            )[0]
            alignment_end_time = min(alignment_end_time, trial_stop)
        else:
            alignment_end_time = trial_stop

        alignment_start_time += alignment_spec["start_time_shift"]
        alignment_event_time += alignment_spec["alignment_time_shift"]
        alignment_end_time += alignment_spec["end_time_shift"]

        alignment_times.append(
            {
                "trial_key": trial_key,
                "start": alignment_start_time,
                "event": alignment_event_time,
                "end": alignment_end_time,
            }
        )

    return pd.DataFrame(alignment_times)
