from typing import Optional


class Version:
    """
    Basic class built for versioning and version comparisons.
    """
    def __init__(
        self,
        major: int,
        minor: int = 0,
        patch: int = 0,
        additional_info: Optional[str] = None
        ):
        if type(major) == str:
            self.__dict__.update(self.parse(major).__dict__)
        else:
            self.set_values(major, minor, patch, additional_info)

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"\
               f"{f' ({self.additional_info})' if self.additional_info else ''}"

    @staticmethod
    def parse(version_string: str):
        """
        Constructs a Version object out of an appropriate version string (e.g. 'Version 1.3.2a').
        """
        beginning, minor, end = version_string.split('.', 2)
        additional_info = None

        major = ''.join([char for char in beginning[::-1] if char.isnumeric()][::-1])
        patch = []
                       
        for index, char in enumerate(end):
            if char.isalpha():
                additional_info = end[index:]
                break
            patch.append(char)
        patch = ''.join(patch)
        
        major = int(major) if major != '' else 0
        minor = int(minor)
        patch = int(patch) if patch != '' else 0
        return Version(major, minor, patch, additional_info)

    def set_values(
        self,
        major: int,
        minor: int = 0,
        patch: int = 0,
        additional_info: Optional[str] = None
        ):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.additional_info = additional_info
        
    def shift_major(self, value=1):
        """
        Increases or decreases the value of the major part of the version
        by the specified value.
        """
        self.major += value

    def shift_minor(self, value=1):
        """
        Increases or decreases the value of the minor part of the version
        by the specified value.
        """
        self.minor += value

    def shift_patch(self, value=1):
        """
        Increases or decreases the value of the patch part of the version
        by the specified value.
        """
        self.patch += value

    def _comparator_function(self, comparator: str, other):
        if type(self) != type(other):
            message = f"Invalid type (`{str(type(self))}`) for comparison with a Version."
            raise TypeError(message)
        
        major_fill = max(len(str(self.major)), len(str(other.major)))
        major, major_ = str(self.major).zfill(major_fill), str(other.major).zfill(major_fill)

        minor_fill = max(len(str(self.minor)), len(str(other.minor)))
        minor, minor_ = str(self.minor).zfill(minor_fill), str(other.minor).zfill(minor_fill)
        
        patch_fill = max(len(str(self.patch)), len(str(other.patch)))
        patch, patch_ = str(self.patch).zfill(patch_fill), str(other.patch).zfill(patch_fill)

        a = int(major+minor+patch)
        b = int(major_+minor_+patch_)

        return eval(f'a {comparator} b')

    def __lt__(self, other):
        return self._comparator_function('<', other)

    def __le__(self, other):
        return self._comparator_function('<=', other)

    def __eq__(self, other):
        return self._comparator_function('==', other)

    def __gt__(self, other):
        return self._comparator_function('>', other)

    def __ge__(self, other):
        return self._comparator_function('>=', other)

    
