#
# MIT License
#
# Copyright (c) 2017-2024 Iván de Paz Centeno
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class EndpointMatcherIterator:
    """
    Provides an iterator to match a request path against a defined endpoint pattern,
    extracting and converting path parameters as needed.
    """
    
    def __init__(self, endpoint, path):
        """
        Initializes the iterator with the endpoint pattern and request path.
        :param endpoint: The endpoint pattern defined for route matching.
        :param path: The actual request path to match against the endpoint pattern.
        """
        self._ep_segment_it = iter(endpoint.split("/"))
        self._p_segment_it = iter(path.split("/"))
        self._parser_map = {
            "int": self._parse_int_argument,
            "float": self._parse_float_argument,
            "string": self._parse_string_argument,
            "path": self._parse_path_argument,
        }

    def _parse_argument(self, argument_type='string', ep_segment_it_eos=None):
        return self._parser_map.get(argument_type, 
                                    self._parser_map['string'])(ep_segment_it_eos)
        
    def _parse_int_argument(self, *args, **kwargs):
        p_segment = next(self._p_segment_it)
        
        if p_segment == "":
            raise ValueError("Path segment containing null value")
            
        return int(p_segment)

    def _parse_float_argument(self, *args, **kwargs):
        p_segment = next(self._p_segment_it)
        
        if p_segment == "":
            raise ValueError("Path segment containing null value")
            
        return float(p_segment)

    def _parse_string_argument(self, *args, **kwargs):
        p_segment = next(self._p_segment_it)
        
        if p_segment == "":
            raise ValueError("Path segment containing null value")
            
        return str(p_segment)

    def _parse_path_argument(self, ep_segment_it_eos):
        # We need to iterate over p_segment_it until we find the p_segment_it_eos
        argument = []
        
        try:
            while True:
                p_segment = next(self._p_segment_it)
        
                if p_segment != ep_segment_it_eos:
                    argument.append(p_segment)
                    
                else:    
                    break
            
        except StopIteration:
            if ep_segment_it_eos is not None and len(ep_segment_it_eos) > 0:
                raise KeyError("Unknown path")
            
        return "/".join(argument)

    def __iter__(self):
        """
        Iterates through the endpoint pattern, matching segments against the request path
        and extracting parameters where defined.
        """
        matches = True

        while True:
            try:
                ep_segment = next(self._ep_segment_it)

                ep_special_segment_bool = ep_segment.startswith("<") and ep_segment.endswith(">")
                ep_special_segment_rawname = (ep_special_segment_bool and ep_segment[1:-1]) or ":"
                ep_special_segment_typed = ":" in ep_special_segment_rawname
                ep_special_segment_type, ep_special_segment_name = (ep_special_segment_typed and ep_special_segment_rawname.split(":", 1)) \
                                                                   or f"string:{ep_special_segment_rawname}".split(":")

                try:
                    ep_segment_it_eos = next(self._ep_segment_it) if ep_special_segment_type == "path" else None
                except StopIteration:
                    ep_segment_it_eos = None
                
                if ep_special_segment_bool:
                    argument_name = ep_special_segment_name
                    argument_result = self._parse_argument(ep_special_segment_type, ep_segment_it_eos=ep_segment_it_eos)
                    
                else:
                    argument_name = None
                    argument_result = None

                if not ep_special_segment_bool:# and ep_special_segment_type == "path"):
                    p_segment = next(self._p_segment_it)
                    matches &= ep_segment == p_segment
                else:
                    p_segment = None
                    
                yield matches, ep_segment, argument_name, argument_result
                
            except StopIteration:           
                try:
                    # Path may be longer than the endpoint's definition. If this is the case, we notify the error.  
                    next(self._p_segment_it)
                    yield False, ep_segment, argument_name, argument_result
                
                except StopIteration:
                    pass
            
                break
