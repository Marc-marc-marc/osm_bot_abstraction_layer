#!/usr/bin/python3

from osm_bot_abstraction_layer.generic_bot_retagging import run_simple_retagging_task

def edit_element(tags):
    if tags.get('crossing') == ("island"):
        tags.pop('crossing', None)
        tags['crossing:island'] = "yes"
    return tags

def main():
    run_simple_retagging_task(
        max_count_of_elements_in_one_changeset=10000,
        objects_to_consider_query="""
[out:xml][timeout:3600];
area[name=France][type=boundary][boundary=administrative][admin_level=2]->.a;
(
node["crossing"=island][!"crossing:island"](area.a);
node["crossing"=island]["crossing:island"=yes](area.a);
);
out body;>;out skel qt;
""",
        cache_folder_filepath='/tmp',
        is_in_manual_mode=False,
        changeset_comment='migration noeud crossing=island en crossing:island=yes pour revenir aux valeurs de crossing=traffic_signals <> uncontrolled <> unmarked',
        discussion_url='https://lists.openstreetmap.org/pipermail/talk-fr/2019-July/093403.html',
        osm_wiki_documentation_page='https://wiki.openstreetmap.org/wiki/Automated_edits/frosm#crossing:island',
        edit_element_function=edit_element,
    )

main()
