import numpy as np

def cal_cos_sim(doc_a, doc_b):
    dot_product = np.dot(doc_a, doc_b)
    norm_a = np.linalg.norm(doc_a)
    norm_b = np.linalg.norm(doc_b)
    return dot_product / (norm_a * norm_b)

doc_1 = np.array([0.0923386, 0.0375083, 0.870153117])
doc_2 = np.array([0.0126545, 0.9858852, 0.001466031])
doc_3 = np.array([0.0582242, 0.0381457, 0.903630078])
doc_4 = np.array([0.0144836, 0.9763511, 0.009165313])
doc_5 = np.array([0.1858516, 0.8107631, 0.003385308])
doc_6 = np.array([0.1807888, 0.0018485, 0.817362717])


sim_score = cal_cos_sim(doc_3, doc_6)

print(sim_score)