#%%
class TranslationTable:
    def __init__(self, translation_ranges):
        self.translations = [] # Tuples of (input_start, len, output_offset)
        for (dest_start, src_start, length) in translation_ranges:
            self.translations.append((src_start, length, dest_start - src_start))

        self.translations = sorted(self.translations, key=lambda x: x[0])
        for i in range(len(self.translations)-1):
            assert (self.translations[i][0] + self.translations[i][1]) <= self.translations[i+1][0]
        self.n_ranges = len(self.translations)


    def translate(self, x):
        for (start, l, offset) in self.translations:
            if (x >= start) and (x < (start + l)):
                return x + offset
        return x
    
    def translate_input_range(self, start, l):
        output_ranges = []

        # Seek forward to the next applicable translation range
        ind_trans_rng = 0
        while ind_trans_rng < self.n_ranges:
            s_trans, l_trans, offset = self.translations[ind_trans_rng]
            if start < (s_trans + l_trans):
                if s_trans < start:
                    # We are starting inside a translation range 
                    # Process this one and advance to the next
                    l_new_range = min(s_trans + l_trans - start, l)
                    output_ranges.append([start + offset, l_new_range])
                    start += l_new_range
                    l -= l_new_range
                    ind_trans_rng += 1
                break
            ind_trans_rng += 1


        while l > 0:
            # Process range up until the next translation range
            if ind_trans_rng == self.n_ranges:
                l_new_range = l
            else:
                n_to_next_range = self.translations[ind_trans_rng][0] - start
                l_new_range = min(n_to_next_range, l)
            if l_new_range > 0:
                output_ranges.append([start, l_new_range])
                start += l_new_range
                l -= l_new_range

            # Process the translation range
            if l > 0:
                l_new_range = min(l, self.translations[ind_trans_rng][1])
                output_ranges.append([start + self.translations[ind_trans_rng][2], l_new_range])
                start += l_new_range
                l -= l_new_range
                ind_trans_rng += 1
        return output_ranges
 

with open("input.txt", "r") as f:
    input_seeds = f.readline().strip().replace("seeds: ", "").split(" ")
    input_seeds = [int(x) for x in input_seeds if len(x)]

    state = 0
    groups = []
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        if not line[0].isdigit():
            groups.append([])
        else:
            groups[-1].append([int(x) for x in line.split(" ")])

translations = [TranslationTable(group) for group in groups]

# Part 1
final_locations = []
for x in input_seeds:
    for translation in translations:
        x = translation.translate(x)
    final_locations.append(x)
print(min(final_locations))

# Part 2
x_ranges = [(s, l) for (s, l) in zip(input_seeds[::2], input_seeds[1::2])]
for translation in translations:
    new_ranges = []
    for (s, l) in x_ranges:
        new_ranges += translation.translate_input_range(s, l)
    print(f"In : {x_ranges}")
    print(f"Out: {new_ranges}")
    print("-"*20)
    x_ranges = new_ranges

print(min([r[0] for r in x_ranges]))



        
    
