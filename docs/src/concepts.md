# Concepts

## User Population

Event- & trial-based experiments have an extensive history in behavioral and cognitive
psychology. Fundamentally, data collection is carved up in time according to some
ontology. Researchers may repeat Trial conditions in some manner to improve statistical
power when contrasting a feature of interest versus a neutral baseline. Neuroscientists,
in particular, may be interested in the moments before and after an Event to look at
neurophysiological factors that predict or are predicted by a subject's behavior. What
may differ between research groups is the ontology used to carve up time.

## Event and Trial Time Locking in Neurophysiology

Event-related potentials (ERPs) are a form of measurement associated with
electrophysiological neural signal activity. Typical neural signal patterns are
continuous recordings lasting for the duration of a recording session. ERPs are short
segmented chunks of neural signals that are time locked to particular events of
experimental interest. These segmented chunks can then be stored across all occurences
of a particular event and then can be averaged across all related trials containing the
event type. Typical common events of interest include stimlus or trial onset and motor
response onsets(button press, eye movements, lever licks). ERPs can ultimately be used
to identify patterns of neural activity associated with the responses to the events of
interest.

## Terminology

The language below is tailored to the dependent variable in many neuroscience
experiments, behavior. These concepts could be restated in reference to any modality.

```text
|----------------------------------------------------------------------------|
|-------------------------------- Session ---------------------------------|__
|------------------------------- Recording ------------------------------|____
|----- Block 1 -----|______|----- Block 2 -----|______|----- Block 3 -----|___
| Trial 1 || Trial 2 |____| Trial 3 || Trial 4 |____| Trial 5 |____| Trial 6 |
|_|e1|_|e2||e3|_|e4|__|e5|__|e6||e7||e8||e9||e10||e11|____|e12||e13|_________|
|----------------------------------------------------------------------------|
```

- A **Session** is period during which data is collected.
- A **Recording** is some source of data tied to a single modality (e.g., behavior).
This may or may not fully capture the session depending on recording latencies or
equipment malfunctions.
- **Block** and **Trial** are non-instantaneous subsets of Session whose traits often
repeat across instances. These periods may be combined or contrasted in downstream
analyses.
- Trials may occur within or extend to the intervals between **Blocks**.
- An **Event** (represented with e above) is an optionally instantaneous occurrence
during a **Session**.
- Projects may differ in their need to record event duration (e.g., onset versus
duration of subject behavior)
- **Events** may occur during other categories, or during continuously recorded behavior.


## Key Partnerships

DataJoint has partnered with the following teams to interview key members, and develop
individualized pipelines. By comparing across use-cases, the DataJoint team has
developed a highly adaptable workflow to meet most needs, and trialize analyses within
an existing DataJoint workflow.

- International Brain Lab
- Mesoscale Activity Project (Janelia Research Campus/Baylor College of Medicine/New
York University)
- Jerry Chen Lab (Boston University)
- University of Rochester-New York University-Harvard University U19
- Columbia University U19
- Tobias Rose Lab (University of Bonn)

## Element Features

Features of Element Event include:

- Pairing of upstream sessions with behavioral recordings
- Multiple recorded attributes for phases of interest (see Attribute part tables for
Block and Trial)
- Defining Trial and Event Types as lookup tables
- Optionally activating only the event schema for event-based recording, without Trial
and Block phases.
- An AlignmentEvent table to define the window of interest relative to specific event types.
- Each level of the hierarchy (Block, Trial, Event) is designed to be optional to suit a given experiment's needs. For example usage, visit our
[Array Electrophysiology Workflow](https://github.com/datajoint/workflow-array-ephys/).

## Element Architecture

Each node in the following diagram represents the analysis code in the workflow for
Element Event and corresponding table in the database. Within the workflow, Element
Event connects to upstream Element Session.

![element-event diagram](https://raw.githubusercontent.com/datajoint/element-event/main/images/trial_event_diagram.svg)

### `subject` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/subject))

Although not required, most choose to connect the `Session` table to a `Subject` table.

|  Table  | Description                                |
|   ---   |     ---                                    |
| Subject | Basic information of the research subject. |

### `session` schema ([API docs](https://datajoint.com/docs/elements/element-session/api/element_session/session_with_datetime))

|  Table  | Description                             |
|   ---   |    ---                                  |
| Session | Unique experimental session identifier. |

### `event` schema ([API docs](../api/element_event/event))

Tables related to event related data storage

| Table              | Description                                                  |
|  ---               |    ---                                                       |
| EventType          | Unique event types and descriptions thereof.                 |
| Behavior Recording | Stores information from one recording session.               |
| Event              | Central table for storing all events from recording session. |
| AlignmentEvent     | Stores events aligned to specific event type.                |

### `trial` schema ([API docs](../api/element_event/trial))

Tables related to Session trials. 

| Table | Description                                                        |
|  ---  |    ---                                                             |
| Block | Stores information from custom experimental blocks.                |
| TrialType | Unique trial types and descriptions thereof.                   |
| Trial | A central table for storing all trials from one recording session. |
| BlockTrial | Stores information on trials from experimental blocks.        |
| TrialEvent | Stores information on trials associated with event type.      |

## Element Development

In addition to the key projects listed above, the DataJoint team met with leaders from
both [Neurodata Without Borders](https://www.nwb.org/) and the
[Kepecs Lab](https://sites.wustl.edu/kepecslab/), as these groups have both tackled the
difficulty of developing ontologies that can cover all possible iterations of behavioral
data collection. Our resulting structure is exemplified by the figure below.

## Roadmap

Further development of this Element is community driven. Upon user requests and based on
guidance from the Scientific Steering Group we will add the following features to this
Element:

- Automated import/export from/to common filetypes.
- Tools for synchronizing to reference clocks.
