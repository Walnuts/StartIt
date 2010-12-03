import os

class Project(object):
    structure_tokens = ['$project', '$titlecase', '$lowercase', '$camelcase',\
            '$uppercase']
    specials_tokens = ['$file']

    def __init__(self, cwd, project):
        self.cwd = cwd
        self.project = project

    def _proj_path(self, *args):
        return os.path.join(self.cwd, *args)

    def parse_tree(self, coll, specials={}, collected_filename=""):
        if isinstance(coll, list):
            for part in coll:

                self.parse_tree(part,\
                        specials,\
                        collected_filename)

        elif isinstance(coll, dict):
            for k, v in coll.iteritems():
                fullpath = self._proj_path(collected_filename, k)
                print("Directory: %s\n" % (fullpath,))

                self.parse_tree(v,\
                        specials,\
                        os.path.join(collected_filename, k))

        else:
            if coll is not None:
                fullpath = self._proj_path(collected_filename, coll)
                if coll not in specials.keys():
                    print("File: %s\n" % (fullpath,))
                else:
                    print("File: %s\n\tRule: %s" % (fullpath, specials[coll]))


if __name__ == "__main__":
    from pprint import pprint
    import yaml

    structure_file =\
    """
    - $project:
        - static:
            - css:
                - reset.css
                - type.css
                - site.css
            - javascript:
                - jquery.js
                - application.js
            - images:
        - templates:
            - base.html
        - tests:
            - __init__.py
            - project_tests.py
        - __init__.py
        - main.py
        - controllers.py
        - models.py
        - settings.py
    """

    specials_file =\
    """
    jquery.js : |
        wget -O $file http://code.jquery.com/jquery-1.4.3.min.js
    reset.css : |
        wget -O $file http://meyerweb.com/eric/tools/css/reset/reset.css
    """

    project_structure = yaml.load(structure_file)
    project_specials = yaml.load(specials_file)

    myproj = Project("/Users/pwoolcoc/Projects", "MyProject")
    myproj.parse_tree(project_structure, project_specials)


