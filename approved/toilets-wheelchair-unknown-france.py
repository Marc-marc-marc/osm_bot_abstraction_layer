#!/usr/bin/python3

from osm_bot_abstraction_layer.generic_bot_retagging import run_simple_retagging_task

def edit_element(tags):
    tags.pop('toilets:wheelchair', None)
    return tags

def main():
    run_simple_retagging_task(
        max_count_of_elements_in_one_changeset=10000,
        objects_to_consider_query="""
[out:xml][timeout:3600];
area[name=France][type=boundary][boundary=administrative][admin_level=2]->.a;
nwr["toilets:wheelchair"=unknown](area.a);
out body;>;out skel qt;
""",
        cache_folder_filepath='/tmp',
        is_in_manual_mode=False,
        changeset_comment='suppression de toilets:wheelchair=unknown qui n apporte aucune information par rapport a l absence de l attribut wheelchair',
        discussion_url='https://lists.openstreetmap.org/pipermail/talk-fr/2017-December/087076.html',
        osm_wiki_documentation_page='https://wiki.openstreetmap.org/wiki/Automated_edits/frosm#purge_related_to_wheelchair=unknown',
        edit_element_function=edit_element,
    )

main()
