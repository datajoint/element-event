"""Events are linked to Trials"""

import datajoint as dj
import inspect
import importlib

schema = dj.schema()

_linking_module = None


def activate(
    schema_name, *, create_schema=True, create_tables=True, linking_module=None
):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (str): when True (default), create schema tables in the database
                             if they do not yet exist.
        linking_module (str): a module (or name) containing the required dependencies.

    Dependencies:
    Upstream tables:
        Session: parent table to BehaviorRecording, identifying a recording session.
        Project: the project with which experimental sessions are associated
        Experimenter: the experimenter(s) participating in a given session
                      To supply from element-lab add `Experimenter = lab.User`
                      to your `workflow/pipeline.py` before `session.activate()`
    Functions:
        get_experiment_root_data_dir(): Retrieve the root data director(y/ies) with
                                        behavioral recordings (e.g., bpod files) for
                                        all subject/sessions, returns a string for
                                        full path to the root data directory.
        get_session_directory(session_key: dict): Retrieve the session directory
                                                containing the recording(s) for a
                                                given Session, returns a string for
                                                full path to the session directory
    """

    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), (
        "The argument 'dependency' must" + " be a module or module name"
    )

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
        add_objects=linking_module.__dict__,
    )


# -------------- Functions required by the element-trial   ---------------


def get_experiment_root_data_dir() -> list:
    """Pulls relevant func from parent namespace to specify root data dir(s).

    It is recommended that all paths in DataJoint Elements stored as relative
    paths, with respect to some user-configured "root" director(y/ies). The
    root(s) may vary between data modalities and user machines. Returns a
    full path string to behavioral root data directory or list of strings
    for possible root data directories.

    Returns:
        Paths (list): List of path(s) to root directories for event data
    """
    return _linking_module.get_experiment_root_data_dir()


def get_session_directory(session_key: dict) -> str:
    """Pulls relative function from parent namespace.

    Retrieves the session directory containing the recorded data for a given
    Session. Returns a string for full path to the session directory.

    Returns:
        Session_dir (str): Relative path to session directory
    """

    return _linking_module.get_session_directory(session_key)


# ----------------------------- Table declarations ----------------------


@schema
class EventType(dj.Lookup):
    """Set of unique events present within a recording session

    Attributes:
        event_type ( varchar(32) ): Unique event type.
        event_type_description ( varchar(256) ): Event type description.
    """

    definition = """
    event_type                : varchar(32)
    ---
    event_type_description='' : varchar(256)
    """


@schema
class BehaviorRecording(dj.Manual):
    """Behavior Recordings

    Attributes:
        Session (foreign key): Session primary key.
        recording_start_time (datetime): Start time of recording.
        recording_duration (float): Duration of recording.
        recording_notes ( varchar(256) ): Optional recording related notes.
    """

    definition = """
    -> Session
    ---
    recording_start_time=null : datetime
    recording_duration=null   : float
    recording_notes=''     : varchar(256)
    """

    class File(dj.Part):
        """File IDs and paths associated with a behavior recording

        Attributes:
            BehaviorRecording (foreign key): Behavior recording primary key.
            filepath ( varchar(64) ): file path of video, relative to root data dir.
        """

        definition = """
        -> master
        filepath              : varchar(64)
        """


@schema
class Event(dj.Imported):
    """Automated table with event related information

    WRT: With respect to

    Attributes:
        BehaviorRecording (foreign key): Behavior recording primary key.
        EventType (foreign key): EventType primary key.
        event_start_time (decimal(10, 4)): Time of event onset in seconds, WRT recording start.
        event_end_time (float): Optional. Seconds WRT recording start.
    """

    definition = """
    -> BehaviorRecording
    -> EventType
    event_start_time          : decimal(10, 4)  # (second) relative to recording start
    ---
    event_end_time=null       : float  # (second) relative to recording start
    """

    def make(self, key):
        """Populate based on unique entries in BehaviorRecording and EventType."""
        raise NotImplementedError("For `insert`, use `allow_direct_insert=True`")


@schema
class AlignmentEvent(dj.Manual):
    """Table designed to provide a mechanism for performing event-aligned analyses

    To use entries from trial.Trial, trial_start_time and trial_end_time must be entered
    in the Event table. WRT = With respect to

    Attributes
        alignment_name ( varchar(32) ): Unique alignment name.
        alignment_description ( varchar(1000) ): Optional. Longer description.
        alignment_event_type (foreign key): Event type to align to.
        alignment_time_shift (float): Seconds WRT alignment_event_type
        start_event_type (foreign key): Event before alignment event type
        start_time_shift (float): Seconds WRT start_event_type
        end_event_type (foreign key): Event after alignment event type
        end_time_shift (float): Seconds WRT end_event_type

    """

    definition = """ # time_shift is seconds to shift with respect to (WRT) a variable
    alignment_name: varchar(32)
    ---
    alignment_description='': varchar(1000)  
    -> EventType.proj(alignment_event_type='event_type') # event type to align to
    alignment_time_shift: float                      # (s) WRT alignment_event_type
    -> EventType.proj(start_event_type='event_type') # event before alignment_event_type
    start_time_shift: float                          # (s) WRT start_event_type
    -> EventType.proj(end_event_type='event_type')   # event after alignment_event_type
    end_time_shift: float                            # (s) WRT end_event_type
    """
