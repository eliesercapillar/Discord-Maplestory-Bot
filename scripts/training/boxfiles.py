import os
os.chdir('S:/Repositories/Discord-Maplestory-Bot/data')
number_of_files = len(os.listdir('./'))
# os.system(f"tesseract ENG.MAPLE.exp{0}.png ENG.MAPLE.exp{0} batch.nochop makebox")
# os.system(f"tesseract ENG.MAPLE.exp{1}.png ENG.MAPLE.exp{1} box.train")
# os.system(f"unicharset_extractor ENG.MAPLE.exp1.box")
# os.system(f"echo \"maple 0 0 1 0 0\" > font_properties")
# os.system(f"mftraining -F font_properties -U unicharset -O train.unicharset ENG.MAPLE.exp1.tr")
# os.system(f"cntraining ENG.MAPLE.exp1.tr")
# os.system(f"rename shapetable maple.shapetable")
# os.system(f"rename inttemp maple.inttemp")
# os.system(f"rename pffmtable maple.pffmtable")
# os.system(f"rename normproto maple.normproto")
os.system(f"combine_tessdata maple.")


# for i in range(1, number_of_files):
#     os.system(f"tesseract ENG.MAPLE.exp{i}.png ENG.MAPLE.exp{i} batch.nochop makebox")