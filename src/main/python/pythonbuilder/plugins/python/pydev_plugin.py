#  This file is part of Python Builder
#   
#  Copyright 2011 The Python Builder Team
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
import string

from pythonbuilder.core import init, task, description

_DOT_PROJECT_TEMPLATE = string.Template("""<?xml version="1.0" encoding="UTF-8"?>

<!-- This file has been generated by the Pythonbuilder Pydev Plugin -->

<projectDescription>
    <name>${project_name}</name>
    <comment></comment>
    <projects>
    </projects>
    <buildSpec>
        <buildCommand>
            <name>org.python.pydev.PyDevBuilder</name>
            <arguments>
            </arguments>
        </buildCommand>
    </buildSpec>
    <natures>
        <nature>org.python.pydev.pythonNature</nature>
    </natures>
</projectDescription>
""")

_DOT_PYDEVPROJECT_PATH_LINE_TEMPLATE = string.Template("\t\t<path>/$project_name/$path</path>\n")                                                       

_DOT_PYDEVPROJECT_TEMPLATE = string.Template("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?eclipse-pydev version="1.0"?>

<!-- This file has been generated by the Pythonbuilder Pydev Plugin -->

<pydev_project>
    <pydev_property name="org.python.pydev.PYTHON_PROJECT_INTERPRETER">${interpreter}</pydev_property>
    <pydev_property name="org.python.pydev.PYTHON_PROJECT_VERSION">${version}</pydev_property>
    <pydev_pathproperty name="org.python.pydev.PROJECT_SOURCE_PATH">
$paths    
    </pydev_pathproperty>
</pydev_project>
""")

@init
def init_pydev_plugin (project):
    project.set_property_if_unset("pydev_interpreter_name", "Default")
    project.set_property_if_unset("pydev_version", "python 2.6")

@task
@description("Generates eclipse-pydev development files")
def pydev_generate (project, logger):
    logger.info("Generating Eclipse/ Pydev project files.")
    
    paths = []
    add_property_value_if_present(paths, project, "dir_source_main_python")
    add_property_value_if_present(paths, project, "dir_source_main_scripts")
    add_property_value_if_present(paths, project, "dir_source_unittest_python")
    add_property_value_if_present(paths, project, "dir_source_integrationtest_python")
    
    paths_string = ""
    for path in paths:
        if os.path.exists(path):
            paths_string += _DOT_PYDEVPROJECT_PATH_LINE_TEMPLATE.substitute({"project_name": project.name, "path": path})
    
    values = {
        "project_name": project.name,
        "interpreter": project.expand("$pydev_interpreter_name"),
        "version": project.expand("$pydev_version"),
        "paths": paths_string
    }
    
    with open(project.expand_path(".project"), "w") as project_file:
        logger.debug("Writing %s", project_file.name)
        project_file.write(_DOT_PROJECT_TEMPLATE.substitute(values))

    with open(project.expand_path(".pydevproject"), "w") as pydevproject_file:
        logger.debug("Writing %s", pydevproject_file.name)
        pydevproject_file.write(_DOT_PYDEVPROJECT_TEMPLATE.substitute(values))

def add_property_value_if_present (list, project, property_name):
    if project.has_property(property_name):
        list.append(project.get_property(property_name))
