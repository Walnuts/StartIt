# StartIt - Project Creator

Do you start projects with the same basic skeleton most of the time? That is
what this tool is for. You create a YAML file with the project skeleton and
can then use the `startit` tool to create new projects instantly.

I am just starting this project out so it doesn't actually *do* anything right
now. Here is the planned usage:

Create a YAML file as a project skeleton:

    # project.yaml
    - $project
        - $project$lowercase
            - __init__.py
        - tests
            - $project$lowercase_tests.py
        - docs
            - .gitkeep
        - bin
            - .gitkeep
        - __init__.py
        - setup.py
        - README

Now use the `startit` command to create as projects as you want based on this
skeleton. If you hadn't guessed, `$project` is a placeholder for the project
name, and `$lowercase` is a modifier for that placeholder. Running this 
command:

    $ startit --structure project.yaml MyFirstProject

will generate these directories and files:

    MyFirstProject/
        my_first_project/
            __init__.py
        tests/
            my_first_project_tests.py
        docs/
            .gitkeep
        bin/
            .gitkeep
        __init__.py
        setup.py
        README

* * *

By default, the tool uses `mkdir` and `touch` to create the directories and
files, respectively. However, you can provide an additional YAML file to 
alter this behavior. Here is another project structure definition that I use
for web.py projects:

    # webpy.yaml
    - $project
        - static
            - css
                - reset.css
                - typography.css
                - site.css
            - javascript
                - jquery.js
                - app.js
            - images
                - .gitkeep
        - templates
            - base.html
        - tests
            - __init__.py
            - $project$lowercase_tests.py
        - __init__.py
        - $project$lowercase.py
        - controllers.py
        - models.py
        - settings.py
        - schema.sql
        - README

Now, if I also provide this "specials" file:

    # webpy_specials.yaml
    jquery.js: |
        wget -O $file http://code.jquery.com/jquery-1.4.3.min.js
    reset.css: |
        wget -O $file http://meyerweb.com/eric/tools/css/reset/reset.css

startit will use the provided commands instead of the default `touch` for
`jquery.js` and `reset.css`.

So, 

    $ startit --structure webpy.yaml --specials webpy_specials.yaml MyProject

will generate these directories and files:

    MyProject/
        static/
            css/
                reset.css
                typography.css
                site.css
            javascript/
                jquery.js
                app.js
            images/
                .gitkeep
        templates/
            base.html
        tests/
            __init__.py
            my_project_tests.py
        __init__.py
        my_project.py
        controllers.py
        models.py
        settings.py
        schema.sql
        README

with `jquery.js` and `reset.css` all ready to go!

* * *

This project is still in it's infancy. I will be trying to get an initial 
working version done over the weekend.

* * *

WP
