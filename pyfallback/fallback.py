from __future__ import annotations


class Fallback:
    def __init__(self, obj: any = None, fallback: any = None):
        self._obj = obj
        self._fallback = fallback

    def __getattr__(self, item):
        if self._obj is None:
            return Fallback(fallback=self._fallback)
        try:
            return Fallback(obj=getattr(self._obj, item), fallback=self._fallback)
        except (KeyError, AttributeError):
            return Fallback(fallback=self._fallback)

    def __setattr__(self, key, value):
        if key in ("_obj", "_fallback"):
            super.__setattr__(self, key, value)
        elif self._obj is not None:
            setattr(self._obj, key, value)

    def __delattr__(self, item):
        if self._obj is not None:
            delattr(self._obj, item)

    def __getitem__(self, item) -> Fallback:
        if self._obj is not None:
            try:
                return Fallback(obj=self._obj[item], fallback=self._fallback)
            except KeyError:
                return Fallback(fallback=self._fallback)
        else:
            return Fallback(fallback=self._fallback)

    def __len__(self) -> Fallback:
        if self._obj is not None:
            return Fallback(len(self._obj))
        else:
            return Fallback(fallback=self._fallback)

    def __iter__(self) -> Fallback:
        try:
            if self._obj is not None:
                return Fallback(iter(self._obj))
            else:
                return Fallback(fallback=self._fallback)
        except TypeError:
            # not iterable, try if pyfallback is iter
            try:
                return Fallback(fallback=iter(self._fallback))
            except TypeError:
                return Fallback(fallback=self._fallback)

    def __next__(self) -> Fallback:
        try:
            return Fallback(next(self._obj))
        except TypeError:
            pass
        # obj is None or not iterator, try pyfallback
        try:
            return Fallback(fallback=next(self._fallback))
        except TypeError:
            # pyfallback is not an iterator, try to make it one
            try:
                self._fallback = iter(self._fallback)
                return Fallback(fallback=next(self._fallback))
            except TypeError:
                # both obj and pyfallback does not work
                raise StopIteration

    def __setitem__(self, key, value):
        if self._obj is not None:
            self._obj[key] = value

    def __delitem__(self, key):
        if self._obj is not None:
            del self.get()[key]

    def __call__(self, *args, **kwargs) -> Fallback:
        if self._obj is None:
            return Fallback(fallback=self._fallback)
        try:
            return Fallback(obj=self._obj(*args, **kwargs), fallback=self._fallback)
        except TypeError:
            return Fallback(fallback=self._fallback)

    def get(self) -> any:
        return self._obj if self._obj is not None else self._fallback

    def __str__(self) -> str:
        return str(self.get())

    def __repr__(self) -> str:
        return f"Fallback(obj={self._obj}, fallback={self._fallback})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Fallback):
            return self.get() == other.get()
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.get())

    def __contains__(self, item) -> bool:
        try:
            return item in self._obj
        except TypeError as e1:
            # obj is None or type is not correct to use contains
            try:
                return item in self._fallback
            except TypeError as e2:
                raise TypeError(
                    f"{repr(self)} is not valid for __contains__, because both obj and fallback failed",
                    e1,
                    e2,
                )


class FallbackWrapper:
    def __init__(self, fallback: any = None):
        self.fallback = fallback

    def __call__(self, to_wrap) -> Fallback:
        return Fallback(to_wrap, fallback=self.fallback)
