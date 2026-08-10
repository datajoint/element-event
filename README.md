> ## ⚠️ This is the `datajoint-2.x` branch of a fork
>
> Unofficial fork of [`datajoint/element-event`](https://github.com/datajoint/element-event),
> ported to **DataJoint 2.x**. Not affiliated with DataJoint. See
> [why this branch exists](#why-this-branch-exists) at the bottom.

[![PyPI version](https://badge.fury.io/py/element-event.svg)](http://badge.fury.io/py/element-event)

# DataJoint Element - Experimental trials

+ `element-event` features a DataJoint pipeline design for event, trial, and block management. 

+ `element-event` is not a complete workflow by itself, but rather a modular design of tables and dependencies. 

+ `element-event` can be flexibly attached to any DataJoint workflow.

+ See the [Element Event documentation](https://docs.datajoint.com/elements/element-event/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit <https://docs.datajoint.com/elements/>.  This work is supported by the National Institutes of Health.

## Element architecture

In diagram below, ***BehaviorRecording*** table starts immediately downstream from
***Session***. Recordings can be segmented into both trials, which are assumed to have 
duration, and events, which may be instantaneous. Researchers may find one or both  appropriate for their particular paradigm. A set of trials can be further organized into
blocks, representing a larger span of time. We provide an
[example workflow](https://github.com/datajoint/workflow-trial/) with a
[pipeline script](https://github.com/datajoint/workflow-trial/blob/main/workflow_trial/pipeline.py)
that models combining this Element with the corresponding 
[Element-Session](https://github.com/datajoint/element-session).

### Trial & Event Schemas

![trial and event schemas](./images/trial_event_diagram.svg)

## Installation

+ Install `element-event`
    ```
    pip install element-event
    ```

+ Upgrade `element-event` previously installed with `pip`
    ```
    pip install --upgrade element-event
    ```

<!---
+ Install `element-interface`

    + `element-interface` is a dependency of `element-event`, however it is not 
      contained within `requirements.txt`.

    ```
    pip install "element-interface @ git+https://github.com/datajoint/element-interface"
    ```
-->

## Usage

### Element activation

To activate the `element-event`, one need to provide:

1. Schema names for the event or trial module
2. Upstream Session table: A set of keys identifying a recording session (see [
Element-Session](https://github.com/datajoint/element-session)).
3. Utility functions. See 
[example definitions here](https://github.com/datajoint/workflow-trial/blob/main/workflow_trial/paths.py)

For more detail, check the docstring of the `element-event`:

```python
from element_event import event, trial

help(event.activate)
help(trial.activate)
```

### Element usage

+ See the 
[workflow-calcium-imaging](https://github.com/datajoint/workflow-calcium-imaging), 
[workflow-array-ephys](https://github.com/datajoint/workflow-array-ephys), and 
[workflow-miniscope](https://github.com/datajoint/workflow-miniscope) 
repositories for example usages of `element-event`.

## Citation

+ If your work uses DataJoint and DataJoint Elements, please cite the respective Research Resource Identifiers (RRIDs) and manuscripts.

+ DataJoint for Python or MATLAB
    + Yatsenko D, Reimer J, Ecker AS, Walker EY, Sinz F, Berens P, Hoenselaar A, Cotton RJ, Siapas AS, Tolias AS. DataJoint: managing big scientific data using MATLAB or Python. bioRxiv. 2015 Jan 1:031658. doi: https://doi.org/10.1101/031658

    + DataJoint ([RRID:SCR_014543](https://scicrunch.org/resolver/SCR_014543)) - DataJoint for `<Select Python or MATLAB>` (version `<Enter version number>`)

+ DataJoint Elements
    + Yatsenko D, Nguyen T, Shen S, Gunalan K, Turner CA, Guzman R, Sasaki M, Sitonic D, Reimer J, Walker EY, Tolias AS. DataJoint Elements: Data Workflows for Neurophysiology. bioRxiv. 2021 Jan 1. doi: https://doi.org/10.1101/2021.03.30.437358

    + DataJoint Elements ([RRID:SCR_021894](https://scicrunch.org/resolver/SCR_021894)) - Element Event (version `<Enter version number>`)

---

## Why this branch exists

Upstream `element-event` was last committed on 2025-05-20 and targets DataJoint
`>=0.13`. DataJoint **2.0.0** shipped 2026-02-03 as a self-described complete
rewrite; the current release is 2.3.2. Because the element's dependency pin
admits 2.x, `pip install element-event` on a fresh environment today resolves
DataJoint 2.x and produces an installation in which the element cannot be
imported. No element had a 2.x branch and there was no open migration issue or
PR anywhere in the `datajoint` org when this fork was created.

**This branch is the complete migration, not a backward-compatible subset.**
An earlier version of this fork split the work into a `compat-fixes` branch
(changes that also work on 0.14.x) and this `datajoint-2.x` branch (adding the
2.x-only changes on top). The upstream maintainer's guidance, after reviewing
that split, was not to ship it that way: a schema is either 2.x or pre-2.x,
DataJoint no longer supports pre-2.x, and landing the backward-compatible
subset alone is actively harmful here -- it clears the import error while
leaving any `longblob`/`attach` attributes in place, which silently corrupts
data instead of loudly failing to import. See
[the migration guide](https://docs.datajoint.com/how-to/migrate-to-v20/) for
the authoritative type mapping and phase structure this follows (this is
Phase I: code only, against empty schemas, no production data touched).

Both `compat-fixes` and `datajoint-2.x` now point at the same commit and carry
the same content, kept as two names only so nothing that already referenced
either one breaks.

### Full scope of this branch

| change | count |
|---|---|
| `dj.schema` -> `dj.Schema` | 2 |
| `longblob` -> `<blob>` | 3 |
| `smallint` -> `int16` | 2 |
| `float` -> `float32` | 9 |
| `requirements.txt`: `datajoint>=0.13` -> `datajoint>=2.3` | — |

### The `longblob` change is not cosmetic

Under DataJoint 2.x a `longblob` attribute is a **raw native column**. It
declares without error and the insert succeeds, but a numpy array written to
it comes back as `bytes`:

```
longblob   (as this element declared it)   -> returned type: bytes     round-trip OK: False
<blob>     (the 2.x codec)                 -> returned type: ndarray   round-trip OK: True
```

Nothing raises. There is no warning beyond a generic "consider a core
DataJoint type" notice at declaration time that says nothing about data loss.
Traced upstream in datajoint/datajoint-python#1527: PyMySQL has no encoder for
`np.ndarray` and silently falls back to `str(value)`; the same declaration on
PostgreSQL raises instead of corrupting. See
[datajoint/element-event#48](https://github.com/datajoint/element-event/issues/48)
for the full round-trip evidence.

### Using it

```
pip install git+https://github.com/akshay-jaggi/element-event.git@datajoint-2.x
```

Pin the commit rather than the branch name if you need reproducibility. Every
change was applied mechanically (regex over each table's `definition` string,
scoped so it cannot touch a docstring or a function signature) and then
reviewed line by line; no element behaviour was altered, only attribute-type
spellings that 2.x renamed, replaced, or requires as core types.

Open PR: [datajoint/element-event#47](https://github.com/datajoint/element-event/pull/47).
