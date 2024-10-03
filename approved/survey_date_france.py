#!/usr/bin/python3

from osm_bot_abstraction_layer.generic_bot_retagging import run_simple_retagging_task

def edit_element(tags):
    #tag = 'data:survey'
    #tags['survey:date'] = tags.pop(tag, None)
    tags['survey:date'] = tags["date:survey"]
    tags.pop('date:survey', None)
    tags.pop('source', None)
    return tags

def main():
    run_simple_retagging_task(
        max_count_of_elements_in_one_changeset=5,
        objects_to_consider_query="""
[out:xml][timeout:25000];
area[name=France][type=boundary][boundary=administrative][admin_level=2]->.a;
nwr['date:survey'](area.a);
out body;>;out skel qt;
""",
        cache_folder_filepath='/tmp',
        #objects_to_consider_query_storage_file='/home/marc_marc/osm-bot-abstraction-layer/survey_date_france.osm',
        is_in_manual_mode=False,
        #is_in_manual_mode=True,
        changeset_comment='remplacer l attribut date:survey par l attribut documente et plus courant survey:date',
        discussion_url='https://lists.openstreetmap.org/pipermail/talk-fr/2017-September/086075.html',
        osm_wiki_documentation_page='https://wiki.openstreetmap.org/wiki/Automated_edits/frosm#survey:date',
        edit_element_function=edit_element,
    )

main()
