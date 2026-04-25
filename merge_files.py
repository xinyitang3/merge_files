import os
import glob
import csv

folder = r"C:\Users\k\Desktop"

# ---------- 1. 合并 CSV ----------
csv_files = glob.glob(os.path.join(folder, "*.csv"))
csv_output = os.path.join(folder, "merged.csv")

# 排除输出文件本身
if csv_files and os.path.abspath(csv_output) in [os.path.abspath(f) for f in csv_files]:
    csv_files.remove(csv_output)

if csv_files:
    with open(csv_output, "w", newline="", encoding="utf-8-sig") as outfile:
        writer = csv.writer(outfile)
        header_saved = False

        for file in csv_files:
            enc = "utf-8"
            try:
                with open(file, "r", encoding=enc, newline="") as infile:
                    reader = csv.reader(infile)
                    header = next(reader)
            except StopIteration:
                print(f"跳过空 CSV: {os.path.basename(file)}")
                continue
            except UnicodeDecodeError:
                enc = "gbk"
                try:
                    with open(file, "r", encoding=enc, newline="") as infile:
                        reader = csv.reader(infile)
                        header = next(reader)
                except Exception as e:
                    print(f"读取 CSV 失败: {os.path.basename(file)} ({e})")
                    continue
            except Exception as e:
                print(f"读取 CSV 失败: {os.path.basename(file)} ({e})")
                continue

            if not header_saved:
                writer.writerow(header)
                header_saved = True

            try:
                for row in reader:
                    writer.writerow(row)
            except Exception as e:
                print(f"写入 CSV 行出错: {os.path.basename(file)} ({e})")
                continue

            print(f"已合并 CSV: {os.path.basename(file)} (编码: {enc})")

    print(f"CSV 合并完成，输出: {csv_output}")
else:
    print("未找到任何 CSV 文件")

# ---------- 2. 合并 TXT ----------
txt_files = glob.glob(os.path.join(folder, "*.txt"))
txt_output = os.path.join(folder, "merged.txt")

# 排除输出文件本身
if txt_files and os.path.abspath(txt_output) in [os.path.abspath(f) for f in txt_files]:
    txt_files.remove(txt_output)

if txt_files:
    with open(txt_output, "w", encoding="utf-8-sig") as outfile:
        for file in txt_files:
            enc = "utf-8"
            try:
                with open(file, "r", encoding=enc) as infile:
                    content = infile.read()
            except UnicodeDecodeError:
                enc = "gbk"
                try:
                    with open(file, "r", encoding=enc) as infile:
                        content = infile.read()
                except Exception as e:
                    print(f"读取 TXT 失败: {os.path.basename(file)} ({e})")
                    continue
            except Exception as e:
                print(f"读取 TXT 失败: {os.path.basename(file)} ({e})")
                continue

            outfile.write(content)
            # 如果文件末尾没有换行，补一个，避免多个文件内容粘在一起
            if not content.endswith("\n"):
                outfile.write("\n")
            print(f"已合并 TXT: {os.path.basename(file)} (编码: {enc})")

    print(f"TXT 合并完成，输出: {txt_output}")
else:
    print("未找到任何 TXT 文件")