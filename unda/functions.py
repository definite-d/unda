from copy import copy
from functools import wraps
from typing import Optional, Dict
from warnings import warn

from .constants import RESERVED_NAMES, VERSION as current_version
from .version import Version


def extract_changes(original, changed) -> Optional[Dict]:
    """
    Obtains and returns a dict of changes by comparing two dicts.

    ## Parameters
    ### _original:_
    Dict to compare "changed" against.

    ### _changed:_
    Dict to be compared for differences.
    """
    target_checklist = [(k, changed[k])
                        for k in changed.keys()
                        if k not in RESERVED_NAMES]
    checklist_anomalies = {}
    for key_value, value in target_checklist:
        if original[key_value] != value or key_value not in original.keys():
            checklist_anomalies[key_value] = value
    return checklist_anomalies if len(checklist_anomalies) > 0 else None


def _deprecated(version, deprecation_target='minor', deadline=3, use_instead=None):
    """
    WARNING: Internal use only. No QA for end users.

    Checks the current project version and compares it to the given version.
    
    If the current version is lower than the given version, nothing happens.
    
    If the current version's target value (e.g. minor) is higher or equal to the given version's target
    value, a warning will be triggered.
    """
    def _inner(func):
        def _wrapper(*args, **kwargs):
            
            given_version = Version(version)
            deadline_version = copy(given_version)
            exec(f'deadline_version.shift_{deprecation_target}(deadline)')
            
            if current_version >= deadline_version:
                message = f'`{func.__name__}` needs to be removed; its deprecation version ({deadline_version}) is past due.'
                raise SystemError(message)
            
            elif current_version >= given_version < deadline_version:
                warning = f'The `{func.__name__}` function has been deprecated! It will still work, but will be fully '\
                f'removed in the next{" "+str(deadline)+" " or " "}{deprecation_target} {"releases" if deadline > 1 else "release"}.'\
                f'{" Please use `"+str(use_instead)+"` instead." if use_instead else ""}'
                warn(warning, stacklevel=2)
                func.__doc__  = f'DEPRECATED since version {version}.\n' + func.__doc__
                
            return func(*args, **kwargs)
        return _wrapper
    return _inner
            
