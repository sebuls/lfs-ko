import os

# 설정 값
SRC_DIR = 'en'
LANG = 'ko'
OUTPUT_FILE = 'po4a.conf'

# po4a.conf 헤더 부분
header = f"""[po4a_langs] {LANG}
[po4a_paths] po/lfs.pot $lang:po/lfs-$lang.po

[po4a_alias:docbook] docbook opt:"-M UTF-8 -L UTF-8"
"""

def generate_po4a_conf():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(header + "\n")
        
        # en 디렉터리를 재귀적으로 탐색
        for root, dirs, files in os.walk(SRC_DIR):
            for file in sorted(files):
                if file.endswith('.xml'):
                    # 상대 경로 추출
                    rel_path = os.path.relpath(os.path.join(root, file), start='.')
                    # ko/ 로 바꾼 경로 생성
                    target_path = rel_path.replace('en/', f'{LANG}/', 1)
                    
                    # 설정 줄 쓰기
                    line = f'[type: docbook] {rel_path} $lang:{target_path} opt:"-k 0"\n'
                    f.write(line)

if __name__ == "__main__":
    if os.path.isdir(SRC_DIR):
        generate_po4a_conf()
        print(f"성공: {OUTPUT_FILE} 파일이 생성되었습니다.")
    else:
        print(f"에러: {SRC_DIR} 디렉터리를 찾을 수 없습니다. 먼저 en/ 폴더를 준비해주세요.")
