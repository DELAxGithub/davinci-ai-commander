#!/usr/bin/env python3
"""
DaVinci Resolve 字幕(SRT)インポートテストスクリプト

SRTテキストを受け取り、DaVinci Resolveの字幕トラックに追加する。
- フレームベース (HH:MM:SS:FF) と標準SRT (HH:MM:SS,mmm) の両形式に対応
- DaVinci Resolve Scripting API の字幕関連機能を検証
"""

import sys
import os
import re
import tempfile

# DaVinci Resolve API ロード
sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    # Fallback: fusionscript 直接ロード
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fusionscript",
        "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    )
    fusionscript = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fusionscript)
    dvr_script = fusionscript


def convert_frame_tc_to_srt_tc(tc_str, fps=29.97):
    """フレームベースのタイムコード (HH:MM:SS:FF) を標準SRT形式 (HH:MM:SS,mmm) に変換"""
    parts = tc_str.strip().split(":")
    if len(parts) == 4:
        h, m, s, f = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
        ms = int(f * 1000 / fps)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    elif "," in tc_str:
        # 既に標準SRT形式
        return tc_str.strip()
    else:
        return tc_str.strip()


def parse_srt(srt_text):
    """SRTテキストをパースしてエントリのリストを返す"""
    entries = []
    blocks = re.split(r'\n\s*\n', srt_text.strip())
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        # 1行目: シーケンス番号
        try:
            seq = int(lines[0].strip())
        except ValueError:
            continue
        # 2行目: タイムコード
        tc_match = re.match(r'(.+?)\s*-->\s*(.+)', lines[1])
        if not tc_match:
            continue
        start_tc = tc_match.group(1).strip()
        end_tc = tc_match.group(2).strip()
        # 3行目以降: テキスト
        text = '\n'.join(lines[2:])
        entries.append({
            'seq': seq,
            'start': start_tc,
            'end': end_tc,
            'text': text
        })
    return entries


def convert_srt_to_standard(srt_text, fps=29.97):
    """フレームベースSRTを標準SRT形式に変換"""
    entries = parse_srt(srt_text)
    output_lines = []
    for entry in entries:
        start = convert_frame_tc_to_srt_tc(entry['start'], fps)
        end = convert_frame_tc_to_srt_tc(entry['end'], fps)
        output_lines.append(str(entry['seq']))
        output_lines.append(f"{start} --> {end}")
        output_lines.append(entry['text'])
        output_lines.append('')
    return '\n'.join(output_lines)


def save_srt_file(srt_text, output_path):
    """SRTテキストをファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_text)
    print(f"SRT保存完了: {output_path}")
    return output_path


def test_subtitle_api(resolve, srt_file_path):
    """DaVinci Resolve の字幕関連APIをテスト"""
    print("\n=== DaVinci Resolve 字幕APIテスト ===")

    if not resolve:
        print("ERROR: DaVinci Resolve に接続できません")
        return False

    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        print("ERROR: プロジェクトが開かれていません")
        return False

    print(f"プロジェクト: {project.GetName()}")

    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("ERROR: タイムラインがありません")
        return False

    print(f"タイムライン: {timeline.GetName()}")
    print(f"フレームレート: {timeline.GetSetting('timelineFrameRate')}")

    # 字幕トラック数を確認
    subtitle_count = timeline.GetTrackCount("subtitle")
    print(f"現在の字幕トラック数: {subtitle_count}")

    # 字幕トラックがなければ追加
    if subtitle_count == 0:
        print("字幕トラックを追加中...")
        result = timeline.AddTrack("subtitle")
        print(f"AddTrack('subtitle') 結果: {result}")
        subtitle_count = timeline.GetTrackCount("subtitle")
        print(f"追加後の字幕トラック数: {subtitle_count}")

    # 字幕トラックの既存アイテムを確認
    if subtitle_count > 0:
        items = timeline.GetItemListInTrack("subtitle", 1)
        if items:
            print(f"字幕トラック1のアイテム数: {len(items)}")
            for i, item in enumerate(items[:5]):  # 最初の5つだけ表示
                name = item.GetName() if hasattr(item, 'GetName') else "N/A"
                print(f"  [{i+1}] {name}")
        else:
            print("字幕トラック1にアイテムなし")

    # ImportSubtitleFile が存在するか確認
    print("\n--- API メソッド探索 ---")
    timeline_methods = [attr for attr in dir(timeline) if 'subtitle' in attr.lower() or 'import' in attr.lower() or 'caption' in attr.lower()]
    print(f"字幕/インポート関連メソッド: {timeline_methods}")

    # ImportSubtitleFile を試行
    import_methods = ['ImportSubtitleFile', 'ImportSubtitles', 'ImportSRT']
    for method_name in import_methods:
        if hasattr(timeline, method_name):
            print(f"✅ {method_name} が見つかりました！")
            try:
                method = getattr(timeline, method_name)
                result = method(srt_file_path)
                print(f"  実行結果: {result}")
                return True
            except Exception as e:
                print(f"  実行エラー: {e}")
        else:
            print(f"❌ {method_name} は存在しません")

    # MediaPool 経由でのインポートを試行
    media_pool = project.GetMediaPool()
    print("\n--- MediaPool 経由でのインポート試行 ---")
    try:
        result = media_pool.ImportMedia([srt_file_path])
        if result:
            print(f"✅ MediaPool.ImportMedia 成功: {result}")
        else:
            print(f"❌ MediaPool.ImportMedia 失敗 (None/False)")
    except Exception as e:
        print(f"❌ MediaPool.ImportMedia エラー: {e}")

    # CreateSubtitlesFromAudio の存在確認
    if hasattr(timeline, 'CreateSubtitlesFromAudio'):
        print("\n✅ CreateSubtitlesFromAudio は利用可能")
        print("  (音声から自動字幕生成が可能)")
    else:
        print("\n❌ CreateSubtitlesFromAudio も利用不可")

    print("\n=== テスト結果まとめ ===")
    print("APIによる直接的なSRTインポートは現在サポートされていません。")
    print(f"SRTファイルは以下に保存済みです:")
    print(f"  {srt_file_path}")
    print()
    print("手動インポート手順:")
    print("  1. DaVinci Resolve を開く")
    print("  2. 対象のタイムラインを選択")
    print("  3. メニュー: File > Import > Subtitle...")
    print(f"  4. ファイルを選択: {srt_file_path}")
    print("  5. インポート設定を確認して OK")
    return False


def main():
    # テスト用SRTテキスト (フレームベースタイムコード)
    srt_text = """1
00:01:40:00 --> 00:01:50:07
1930年代 アメリカ AT&T副社長チェスター・バーナードは
ある矛盾に気づいていました

2
00:01:50:17 --> 00:01:58:20
同じ頃 ハーバード大学のホーソン実験が
衝撃的な結果を報告していた

3
00:01:58:20 --> 00:02:02:28
工場の照明を明るくしても暗くしても
生産性が上がる

4
00:02:03:08 --> 00:02:11:04
物理的条件ではなく 観察されているという人間関係が
生産性を左右していたのです

5
00:02:11:14 --> 00:02:13:25
バーナードは確信しました

6
00:02:14:05 --> 00:02:19:15
非公式組織は 公式組織の運営に不可欠である

7
00:02:19:25 --> 00:02:26:25
組織図に載っている関係だけでは
組織は動かない

8
00:02:26:25 --> 00:02:33:25
誰と誰が信頼関係にあるか
誰が情報のハブになっているか

9
00:02:33:25 --> 00:02:37:25
誰が感情的な緩衝材になっているか

10
00:02:37:25 --> 00:02:41:25
ナンバー2の仕事の多くは
この非公式組織の中にあります

11
00:02:41:25 --> 00:02:45:05
議事録にも残らない でも
それがなければ組織は崩壊する

12
00:02:45:15 --> 00:02:50:16
紀元前3世紀 中国・戦国時代

13
00:02:50:16 --> 00:02:55:17
韓の国の王族に生まれた韓非は
吃音のため弁論ができず

14
00:02:55:27 --> 00:02:59:12
代わりに文章で思想を磨きました

15
00:02:59:22 --> 00:03:07:02
彼の著作は 敵国・秦の始皇帝を魅了した

16
00:03:07:02 --> 00:03:14:13
しかし皮肉なことに 韓非は秦に招かれた後
かつての同門・李斯の讒言により獄中で毒を仰ぎます

17
00:03:14:23 --> 00:03:17:01
その韓非が残した言葉

18
00:03:17:11 --> 00:03:21:25
術とは 胸中に蔵するものなり

19
00:03:22:05 --> 00:03:29:17
本当の影響力は
目に見える命令や権限の中にはない

20
00:03:29:17 --> 00:03:34:29
相手に自分が決めたと思わせながら
実は状況全体を整えている

21
00:03:34:29 --> 00:03:38:11
そんな見えない力

22
00:03:38:11 --> 00:03:43:23
現代の組織で その術を実際に使っているのは
誰でしょうか

23
00:03:43:23 --> 00:03:47:05
上司が自分で決断したと思っている

24
00:03:47:05 --> 00:03:51:17
でも実は その決断に必要な情報を揃え
選択肢を絞り タイミングを計っていたのは

25
00:03:51:17 --> 00:03:54:12
影にいるあなたかもしれません

26
00:03:54:22 --> 00:04:03:14
1643年 肥後国・熊本
晩年の宮本武蔵は 霊巌洞という洞窟にこもり

27
00:04:03:24 --> 00:04:10:10
生涯の兵法をまとめていました

28
00:04:10:10 --> 00:04:14:27
死の直前まで書き続けた五輪書
その水之巻にこうあります

29
00:04:15:07 --> 00:04:19:22
水を手本として 心を水のようにせよ

30
00:04:20:02 --> 00:04:26:21
水は 器に従って形を変える

31
00:04:26:21 --> 00:04:31:11
四角い器なら四角に 丸い器なら丸く

32
00:04:31:11 --> 00:04:35:01
しかし その柔軟さこそが強さです

33
00:04:35:01 --> 00:04:38:28
岩を穿つのは 硬い鉄ではなく
柔らかい水の滴り

34
00:04:39:08 --> 00:04:45:23
ナンバー2に求められるのは
この水の性質かもしれません

35
00:04:45:23 --> 00:04:50:19
状況に応じて形を変え 隙間に入り込み
障害を迂回する

36
00:04:50:19 --> 00:04:56:11
自己主張しない でも 確実に浸透していく

37
00:04:56:21 --> 00:05:00:19
化学に触媒という概念があります

38
00:05:00:29 --> 00:05:09:00
20世紀初頭 ドイツの化学者
フリッツ・ハーバーとカール・ボッシュは

39
00:05:09:00 --> 00:05:15:05
空気中の窒素からアンモニアを合成する方法を
発見しました
鍵となったのは鉄触媒

40
00:05:15:15 --> 00:05:21:20
この発見は 世界の食糧生産を一変させ
ノーベル賞を受賞します

41
00:05:21:20 --> 00:05:27:26
しかし 生成されたアンモニアの中に
鉄の痕跡は残りません

42
00:05:28:06 --> 00:05:34:24
触媒とは 反応を加速させるが
自分自身は変化しない物質

43
00:05:34:24 --> 00:05:38:19
なければ反応は起こらない でも
成果物に名前は刻まれない

44
00:05:38:19 --> 00:05:41:25
ナンバー2の仕事は 触媒に似ています

45
00:05:41:25 --> 00:05:50:00
自分がいなくても同じだったは 錯覚です

46
00:05:50:10 --> 00:06:02:18
1915年 デンマーク
心理学者エドガー・ルビンは 博士論文で
図と地という知覚の法則を発表しました

47
00:06:02:28 --> 00:06:08:02
有名なルビンの壺

48
00:06:08:02 --> 00:06:13:05
白い部分を見れば壺が見える
黒い部分を見れば向かい合う二つの顔が見える

49
00:06:13:15 --> 00:06:19:09
どちらが図で どちらが地かは
見方によって反転する

50
00:06:19:09 --> 00:06:25:03
そして重要なのは 地がなければ
図は存在できないということ

51
00:06:25:03 --> 00:06:31:03
背景があるから 主役が浮かび上がる

52
00:06:31:13 --> 00:06:37:20
ナンバー2は地かもしれません
でも 地なき図はありえない

53
00:06:37:20 --> 00:06:41:27
あなたがいるから 上司は図として輝ける

54
00:06:42:07 --> 00:06:49:14
それは従属ではありません
図と地は 互いを成り立たせている
対等な関係なのです

55
00:06:49:24 --> 00:06:55:22
明日も会議がある
上司が発言し あなたは横で控えている

56
00:06:56:02 --> 00:06:59:29
でも 少しだけ視点を変えてみてください

57
00:07:00:09 --> 00:07:14:16
あなたは非公式組織の結節点であり
見えない術の使い手であり
形を持たない水であり
反応を加速させる触媒であり
主役を浮かび上がらせる地である

58
00:07:14:26 --> 00:07:20:20
ナンバー2であることは
劣っていることではない

59
00:07:20:20 --> 00:07:25:13
それは 誰にも見えない場所で
組織という絵画を成り立たせていることなのです

60
00:07:25:23 --> 00:07:32:21
夜空を見上げると オリオン座が輝いています

61
00:07:32:21 --> 00:07:37:19
私たちが見ているのは 明るい星だけ

62
00:07:37:19 --> 00:07:40:10
でも その星々の間には
見えない暗黒物質が満ちている

63
00:07:40:20 --> 00:07:47:05
宇宙の構造を支えているのは 光ではなく
見えない質量なのです

64
00:07:47:05 --> 00:07:53:17
知識の星座は
見る人によって違う物語を紡ぎます

65
00:07:53:27 --> 00:07:59:14
今夜 あなたの見えない仕事に
静かな誇りが灯りますように"""

    # --- ステップ1: SRTファイルの準備 ---
    project_dir = "/Users/delaxstudio/src/delax-ops/ops/media/orion/projects/OrionEp22/output"

    # フレームベース版を保存 (そのまま)
    frame_srt_path = os.path.join(project_dir, "OrionEp22_subtitle_frames.srt")
    save_srt_file(srt_text, frame_srt_path)

    # 標準SRT形式に変換して保存 (29.97fps)
    standard_srt = convert_srt_to_standard(srt_text, fps=29.97)
    standard_srt_path = os.path.join(project_dir, "OrionEp22_subtitle.srt")
    save_srt_file(standard_srt, standard_srt_path)

    print(f"\n変換サンプル (最初の3エントリ):")
    for line in standard_srt.split('\n')[:12]:
        print(f"  {line}")

    # --- ステップ2: DaVinci Resolve APIテスト ---
    try:
        resolve = dvr_script.scriptapp("Resolve")
        test_subtitle_api(resolve, standard_srt_path)
    except Exception as e:
        print(f"\nDaVinci Resolve 接続エラー: {e}")
        print("DaVinci Resolve が起動していることを確認してください。")
        print(f"\nSRTファイルは保存済みです:")
        print(f"  標準形式: {standard_srt_path}")
        print(f"  フレーム形式: {frame_srt_path}")


if __name__ == "__main__":
    main()
