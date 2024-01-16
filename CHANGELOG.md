# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.3.1] - 2024-01-12

+ Update - `BehaviorRecording.File` table's attribute `filepath` length to `varchar(256)`

## [0.3.0] - 2023-11-09

+ Add - `BehaviorTimeSeries` table

## [0.2.3] - 2023-06-20

+ Update - GitHub Actions workflows
+ Fix - Remove Google Analytics key
+ Add - GitHub Issue Templates

## [0.2.2] - 2023-05-11

+ Fix - `.ipynb` dark mode output for all notebooks.
+ Fix - Remove `GOOGLE_ANALYTICS_KEY` from `u24_element_release_call.yml`.

## [0.2.1] - 2023-04-28

+ Fix - `.ipynb` output in tutorials is not visible in dark mode.

## [0.2.0] - 2023-04-04

+ Update - `event.Event::event_start_time` datatype to decimal(10, 4)

## [0.1.3] - 2022-11-02

+ Add - mkdocs deployment

## [0.1.2] - 2022-08-26

+ Add - `attribute_blob` as `longblob` in the Attribute tables
+ Add - support storing non-string data types

## [0.1.1] - 2022-06-10

+ Add - NotImplementedError where Imported tables do not offer make function
+ Add - get_trialized_alignment_event_times docstring specificity
+ Update - Diagram to reflect design with trial.BlockTrial as imported

## [0.1.0] - 2022-05-10

+ Add - Draft based on [Cajal](https://github.com/cajal/pipeline) and [Kavli Institute](https://github.com/kavli-ntnu/dj-docs) precursor projects
+ Add - Table architecture
+ Add - AlignmentEvent design to capture windows relative to an event
+ Add - Black formatting into code base

[0.3.0]: https://github.com/datajoint/element-event/releases/tag/0.3.0
[0.2.3]: https://github.com/datajoint/element-event/releases/tag/0.2.3
[0.2.2]: https://github.com/datajoint/element-event/releases/tag/0.2.2
[0.2.1]: https://github.com/datajoint/element-event/releases/tag/0.2.1
[0.2.0]: https://github.com/datajoint/element-event/releases/tag/0.2.0
[0.1.3]: https://github.com/datajoint/element-event/releases/tag/0.1.3
[0.1.2]: https://github.com/datajoint/element-event/releases/tag/0.1.2
[0.1.1]: https://github.com/datajoint/element-event/releases/tag/0.1.1
[0.1.0]: https://github.com/datajoint/element-event/releases/tag/0.1.0
