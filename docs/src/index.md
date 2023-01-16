# Element Event

DataJoint Element for session related Event Management. DataJoint Elements collectively standardize and automate data collection and analysis for neuroscience experiments. Each Element is a modular pipeline for data storage and processing with corresponding database tables that can be combined with other Elements to assemble a fully functional pipeline.

Element Event features a DataJoint pipeline allowing for a standard approach for session
level organization. The Element is composed of two schemas for storing data:

- `event` - Manages event related data storage

- `trial` - Manages trial related data storage

Visit the [Concepts page](./concepts.md) for more information on 
session management and Element Session.  To get started with building your data pipeline visit the [Tutorials page](./tutorials.md).

![element-event diagram](https://raw.githubusercontent.com/datajoint/element-event/main/images/trial_event_diagram.svg)