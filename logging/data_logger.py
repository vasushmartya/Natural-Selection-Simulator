import csv

class DataLogger:
    def __init__(self, filename="natural_selection_data.csv"):
        self.filename = filename
        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "Tick", "Total Creatures", 
                "Speed_SS", "Speed_Ss", "Speed_ss", 
                "Vision_VV", "Vision_Vv", "Vision_vv", 
                "Beauty_AA", "Beauty_Aa", "Beauty_aa",
                "Violence_KK", "Violence_Kk", "Violence_kk"
            ])

    def update(self, world):
        if world.tick % 20 != 0:
            return

        speed_SS, speed_Ss, speed_ss = 0, 0, 0
        vision_VV, vision_Vv, vision_vv = 0, 0, 0
        beauty_AA, beauty_Aa, beauty_aa = 0, 0, 0
        violent_KK, violent_Kk, violent_kk = 0, 0, 0
        
        for c in world.creatures:
            # Track Speed
            s_genes = "".join(sorted(c.genes["speed"]))
            if s_genes == "SS": speed_SS += 1
            elif s_genes == "Ss": speed_Ss += 1
            else: speed_ss += 1
                
            # Track Vision
            v_genes = "".join(sorted(c.genes["vision"]))
            if v_genes == "VV": vision_VV += 1
            elif v_genes == "Vv": vision_Vv += 1
            else: vision_vv += 1

            # Track Beauty
            a_genes = "".join(sorted(c.genes["attractiveness"]))
            if a_genes == "AA": beauty_AA += 1
            elif a_genes == "Aa": beauty_Aa += 1
            else: beauty_aa += 1

            # Track Violence
            k_genes = "".join(sorted(c.genes["violence"]))
            if k_genes == "KK": violent_KK += 1
            elif k_genes == "Kk": violent_Kk += 1
            else: violent_kk += 1
            
        print(f"Total creatures: {len(world.creatures)}")
        print(f"SPEED | Fast (SS): {speed_SS} | Fast (Ss): {speed_Ss} | Slow (ss): {speed_ss}")
        print(f"SIGHT | Blind (VV): {vision_VV} | Blind (Vv): {vision_Vv} | Eagle-Eyed (vv): {vision_vv}")
        print(f"Attractivness | Hot (AA): {beauty_AA} | Ugly (Aa): {beauty_Aa} | Ugly (aa): {beauty_aa}")
        print(f"Violence | Strong (KK): {violent_KK} | Hybrid (Kk): {violent_Kk} | Peaceful (kk): {violent_kk}")
        print(f"kill count = {world.kill_count}")
        print("-" * 40)

        with open(self.filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                world.tick, len(world.creatures),
                speed_SS, speed_Ss, speed_ss,
                vision_VV, vision_Vv, vision_vv,
                beauty_AA, beauty_Aa, beauty_aa,
                violent_KK, violent_Kk, violent_kk
            ])