import jsonlines
import rltk
import time
import re


def compare_cpu(g2a_min_cpu_1, techpowerup_cpu, g2a_min_cpu_2=None, max_score_1=-1, max_score_2=-1):
    # techpowerup_cpu_reader = jsonlines.open(techpowerup_cpu, 'r')
    similar_id_1 = ''
    similar_id_2 = ''
    most_similar_cpu_1 = ''
    most_similar_cpu_2 = ''
    score_1 = -9999
    score_2 = -9999
    with jsonlines.open(techpowerup_cpu, 'r') as techpowerup_cpu_reader:
        if g2a_min_cpu_1 != None and g2a_min_cpu_2 != None:

            for cpu in techpowerup_cpu_reader:
                cpu_key, cpu_value = list(cpu.items())[0][0], list(cpu.items())[0][1]
                if len(g2a_min_cpu_1) != 0:
                    score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,
                                                          cpu_value['name'].lower()) + rltk.jaro_winkler_similarity(
                        g2a_min_cpu_1, cpu_value['name'].lower())
                '''if "Intel" in g2a_min_cpu_1:
                    if cpu_value["Company"] == "Intel":
                        score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])
                elif "AMD" in g2a_min_cpu_1:
                    if cpu_value["Company"] == 'AMD':
                        score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])
                else:
                    score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])'''

                if len(g2a_min_cpu_2) != 0:
                    score_2 = rltk.levenshtein_similarity(g2a_min_cpu_2,
                                                          cpu_value['name'].lower()) + rltk.jaro_winkler_similarity(
                        g2a_min_cpu_2, cpu_value['name'].lower())

                '''if "Intel" in g2a_min_cpu_2:
                    if cpu_value["Company"] == "Intel":
                        score_2 = rltk.levenshtein_similarity(g2a_min_cpu_2,cpu_value['name'])
                elif "AMD" in g2a_min_cpu_2:
                    if cpu_value["Company"] == 'AMD':
                        score_2 = rltk.levenshtein_similarity(g2a_min_cpu_2,cpu_value['name'])
                else:
                    score_2 = rltk.levenshtein_similarity(g2a_min_cpu_2,cpu_value['name'])'''
                # score_2 = rltk.levenshtein_similarity(g2a_min_cpu_2,cpu_value['name'])

                if score_1 > max_score_1:
                    max_score_1 = score_1
                    similar_id_1 = cpu_key
                    most_similar_cpu_1 = cpu_value['name']

                if score_2 > max_score_2:
                    max_score_2 = score_2
                    similar_id_2 = cpu_key
                    most_similar_cpu_2 = cpu_value['name']

            if max_score_1 >= 1.2 and max_score_2 >= 1.2:
                return {
                    'most_sim_cpu_1': {'name': most_similar_cpu_1, 'sim_id': similar_id_1, 'sim_score': max_score_1},
                    'most_sim_cpu_2': {'name': most_similar_cpu_2, 'sim_id': similar_id_2, 'sim_score': max_score_2}}

            elif max_score_1 >= 1.2 and max_score_2 <= 1.2:
                return {
                    'most_sim_cpu_1': {'name': most_similar_cpu_1, 'sim_id': similar_id_1, 'sim_score': max_score_1},
                    'most_sim_cpu_2': {'name': '', 'sim_id': '', 'sim_score': max_score_2}}

            elif max_score_1 <= 1.2 and max_score_2 >= 1.2:
                return {'most_sim_cpu_1': {'name': '', 'sim_id': '', 'sim_score': max_score_1},
                        'most_sim_cpu_2': {'name': most_similar_cpu_2, 'sim_id': similar_id_2,
                                           'sim_score': max_score_2}}

            else:
                return {'most_sim_cpu_1': {'name': '', 'sim_id': '', 'sim_score': max_score_1},
                        'most_sim_cpu_2': {'name': '', 'sim_id': '', 'sim_score': max_score_2}}

        if g2a_min_cpu_1 != None and g2a_min_cpu_2 == None:
            for cpu in techpowerup_cpu_reader:
                cpu_key, cpu_value = list(cpu.items())[0][0], list(cpu.items())[0][1]

                if len(g2a_min_cpu_1) != 0:
                    score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,
                                                          cpu_value['name']) + rltk.jaro_winkler_similarity(
                        g2a_min_cpu_1, cpu_value['name'].lower())

                '''if "Intel" in g2a_min_cpu_1:
                    if cpu_value["Company"] == "Intel":
                        score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])
                elif "AMD" in g2a_min_cpu_1:
                    if cpu_value["Company"] == 'AMD':
                        score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])
                else:
                    score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1,cpu_value['name'])'''
                # score_1 = rltk.levenshtein_similarity(g2a_min_cpu_1, cpu_value['name'])
                if score_1 > max_score_1:
                    max_score_1 = score_1
                    similar_id_1 = cpu_key
                    most_similar_cpu_1 = cpu_value['name']
            if max_score_1 >= 1.2:
                return {'most_sim_cpu': {'name': most_similar_cpu_1, 'sim_id': similar_id_1, 'sim_score': max_score_1}}
            else:
                return {'most_sim_cpu': {'name': '', 'sim_id': '', 'sim_score': max_score_1}}


def clean_cpu_string1(cpu_1, cpu_2=None):
    if cpu_2 != None:
        cpu_1 = re.sub("@\d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("@ \d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("\d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("\d*\.?\d+(ghz)", "", cpu_1).strip()
        cpu_1 = re.sub('\d (ghz)', '', cpu_1).strip()
        cpu_1 = re.sub('intel', '', cpu_1).strip()
        cpu_1 = re.sub('amd', '', cpu_1).strip()
        cpu_1 = re.sub(' or ', '', cpu_1).strip()
        cpu_1 = re.sub('equivalent', '', cpu_1).strip()
        cpu_1 = re.sub('higher', '', cpu_1).strip()
        cpu_1 = re.sub('better', '', cpu_1).strip()
        cpu_1 = re.sub('-', '', cpu_1).strip()
        cpu_1 = cpu_1.replace("®", "").strip()

        cpu_2 = re.sub("@\d*\.?\d+ (ghz)", "", cpu_2).strip()
        cpu_2 = re.sub("@ \d*\.?\d+ (ghz)", "", cpu_2).strip()
        cpu_2 = re.sub("\d*\.?\d+ (ghz)", "", cpu_2).strip()
        cpu_2 = re.sub("\d*\.?\d+(ghz)", "", cpu_2).strip()
        cpu_2 = re.sub('\d (ghz)', '', cpu_2).strip()
        cpu_2 = re.sub('intel', '', cpu_2).strip()
        cpu_2 = re.sub('amd', '', cpu_2).strip()
        cpu_2 = re.sub(' or ', '', cpu_2).strip()
        cpu_2 = re.sub('equivalent', '', cpu_2).strip()
        cpu_2 = re.sub('higher', '', cpu_2).strip()
        cpu_2 = re.sub('better', '', cpu_2).strip()
        cpu_2 = re.sub('-', '', cpu_2).strip()
        cpu_2 = cpu_2.replace("®", "").strip()

        return cpu_1, cpu_2

    else:
        cpu_1 = re.sub("@\d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("@ \d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("\d*\.?\d+ (ghz)", "", cpu_1).strip()
        cpu_1 = re.sub("\d*\.?\d+(ghz)", "", cpu_1).strip()
        cpu_1 = re.sub('\d (ghz)', '', cpu_1).strip()
        cpu_1 = re.sub('intel', '', cpu_1).strip()
        cpu_1 = re.sub('amd', '', cpu_1).strip()
        cpu_1 = re.sub(' or ', '', cpu_1).strip()
        cpu_1 = re.sub('equivalent', '', cpu_1).strip()
        cpu_1 = re.sub('higher', '', cpu_1).strip()
        cpu_1 = re.sub('better', '', cpu_1).strip()
        cpu_1 = re.sub('-', '', cpu_1).strip()
        cpu_1 = cpu_1.replace("®", "").strip()

        return cpu_1


if __name__ == '__main__':
    st = time.time()
    # g2a_directory = '../data_supporting/g2a_id_min_requirement_mapping.jl'
    # techpowerup_cpu = '../data_with_ids/techpowerup_cpu.jl'
    # er_data_directory =  '../data_er/g2a_game_techpowerup_cpu_er.jl'
    # g2a_reader = jsonlines.open(g2a_directory,'r')

    g2a_directory = 'g2a_id_min_requirement_mapping.jl'
    techpowerup_cpu = 'techpowerup_cpu.jl'
    er_data_directory = 'g2a_game_techpowerup_cpu_er_v3.jl'

    er_writer = jsonlines.open(er_data_directory, 'w')
    with jsonlines.open(g2a_directory, 'r') as g2a_reader:
        for i, game in enumerate(g2a_reader):
            if i % 100 == 0:
                time_elapsed = time.time() - st
                print('time taken for {} is {}'.format(i, time_elapsed))

            key, val = list(game.items())[0][0], list(game.items())[0][1]
            if "Processor" in val:
                if ' or ' in val["Processor"]:
                    max_score_1 = -1
                    max_score_2 = -1
                    # print(val['Processor'])
                    g2a_min_cpu_1 = val["Processor"].split(' or ')[0].strip().lower()
                    g2a_min_cpu_2 = val["Processor"].split(' or ')[1].strip().lower()
                    g2a_min_cpu_1, g2a_min_cpu_2 = clean_cpu_string1(g2a_min_cpu_1, g2a_min_cpu_2)
                    # print('cpu cleaned: ',g2a_min_cpu_1,g2a_min_cpu_2)
                    sim_dic = compare_cpu(g2a_min_cpu_1, techpowerup_cpu, g2a_min_cpu_2, max_score_1, max_score_2)

                    er_writer.write({'g2a': {'id': key, 'Processor': val['Processor']}, 'similarity': sim_dic})

                elif '/' in val["Processor"]:
                    max_score_1 = -1
                    max_score_2 = -1
                    # print(val['Processor'])
                    g2a_min_cpu_1 = val["Processor"].split('/')[0].strip().lower()
                    g2a_min_cpu_2 = val['Processor'].split('/')[1].strip().lower()
                    g2a_min_cpu_1, g2a_min_cpu_2 = clean_cpu_string1(g2a_min_cpu_1, g2a_min_cpu_2)
                    # print('cpu cleaned: ',g2a_min_cpu_1,g2a_min_cpu_2)
                    sim_dic = compare_cpu(g2a_min_cpu_1, techpowerup_cpu, g2a_min_cpu_2, max_score_1, max_score_2)
                    er_writer.write({'g2a': {'id': key, 'Processor': val['Processor']}, 'similarity': sim_dic})

                else:
                    max_score_1 = -1
                    g2a_min_cpu_1 = val["Processor"].strip().lower()
                    g2a_min_cpu_1 = clean_cpu_string1(g2a_min_cpu_1)
                    # print('cpu cleaned: ',g2a_min_cpu_1)
                    sim_dic = compare_cpu(g2a_min_cpu_1, techpowerup_cpu, max_score_1=max_score_1)
                    er_writer.write({'g2a': {'id': key, 'Processor': val['Processor']}, 'similarity': sim_dic})
            else:
                er_writer.write({'g2a': {'id': key}, 'similarity': {'sim_score': -1}})







