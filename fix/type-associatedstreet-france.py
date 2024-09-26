#!/usr/bin/python3

from osm_bot_abstraction_layer.generic_bot_retagging import run_simple_retagging_task

def edit_element(tags):
    if tags.get('type') == ("associatedstreet"):
        tags['type'] = "associatedStreet"
    return tags

def main():
    run_simple_retagging_task(
        max_count_of_elements_in_one_changeset=10000,
        objects_to_consider_query="""
[out:xml][timeout:60];
area[name=France][type=boundary][boundary=administrative][admin_level=2]->.a;
relation[type=associatedstreet](area.a);
out body;>;out skel qt;
""",
        cache_folder_filepath='/tmp',
        is_in_manual_mode=False,
        changeset_comment='correction bug iD type=associatedstreet -> type=associatedStreet',
        discussion_url='https://github.com/openstreetmap/iD/issues/9639',
        osm_wiki_documentation_page='https://github.com/openstreetmap/iD/issues/9639',
        edit_element_function=edit_element,
    )

main()
