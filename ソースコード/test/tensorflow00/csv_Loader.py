import csv

def csv_loader(filename):
    csv_obj = csv.reader(open(filename, "r"))
    dt = [v for v in csv_obj]
    dat = [[float(elm) for elm in v] for v in dt]
    db = [[0 for n in range(5)] for m in range(len(dat))]
    lb = [[0 for nn in range(2)] for mm in range(len(dat))]
    for i in range(len(dat)):
        for j in range(len(dat[i])):
            if j <= 4:
                db[i][j] = dat[i][j]
            else:
                lb[i][j - 5] = dat[i][j]
    return (db, lb)

if __name__ =="__main__":

    csv_loader("USDJPY.csv")

    print(db)
    print(lb)
