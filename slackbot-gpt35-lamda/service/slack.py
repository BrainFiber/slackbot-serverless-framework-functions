import logging
import os
from slack_bolt import App, Ack
from slack_sdk.web import WebClient
from service.gpt import gpt35

app = App(
    # リクエストの検証に必要な値
    # Settings > Basic Information > App Credentials > Signing Secret で取得可能な値
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # 上でインストールしたときに発行されたアクセストークン
    # Settings > Install App で取得可能な値
    token=os.environ["SLACK_BOT_TOKEN"],
    # AWS Lamdba では、必ずこの設定を true にしておく必要があります
    process_before_response=True,
)


# グローバルショットカット実行に対して、ただ ack() だけを実行する関数
# lazy に指定された関数は別の AWS Lambda 実行として非同期で実行されます
def just_ack(ack: Ack):
    ack()


# グローバルショットカット実行に対して、非同期で実行される処理
# trigger_id は数秒以内に使う必要があるが、それ以外はいくら時間がかかっても構いません
def start_modal_interaction(body: dict, client: WebClient):
    # 入力項目ひとつだけのシンプルなモーダルを開く
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "My App"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "element": {"type": "plain_text_input"},
                    "label": {"type": "plain_text", "text": "Text"},
                },
            ],
        },
    )


# モーダルで送信ボタンが押されたときに呼び出される処理
# このメソッドは 3 秒以内に終了しなければならない
def handle_modal(ack: Ack):
    # ack() は何も渡さず呼ぶとただ今のモーダルを閉じるだけ
    # response_action とともに応答すると
    # エラーを表示したり、モーダルの内容を更新したりできる
    # https://slack.dev/bolt-python/ja-jp/concepts#view_submissions
    ack()


# モーダルで送信ボタンが押されたときに非同期で実行される処理
# モーダルの操作以外で時間のかかる処理があればこちらに書く
def handle_time_consuming_task(logger: logging.Logger, view: dict):
    logger.info(view)


# @app.view のようなデコレーターでの登録ではなく
# Lazy Listener としてメインの処理を設定します
app.shortcut("run-aws-lambda-app")(
    ack=just_ack,
    lazy=[start_modal_interaction],
)
app.view("modal-id")(
    ack=handle_modal,
    lazy=[handle_time_consuming_task],
)


def mention_event_ack(body, say, ack, client):
    just_ack(ack)

    mention = body["event"]
    text = mention["text"]
    channel = mention["channel"]
    ts = mention["ts"]
    thread_ts = mention.get("thread_ts")

    parent_ts = thread_ts if thread_ts else ts

    client.reactions_add(name="eyes", channel=channel, timestamp=ts)

    # スレッドのチャット履歴を保存する変数を定義
    thread_history = {}

    if thread_ts:  # メンションがスレッド内で行われた場合
        # スレッドのメッセージを取得
        thread_history = client.conversations_replies(channel=channel, ts=thread_ts)
    # スレッドのチャット履歴を保存する変数を文字列で保存する変数を定義
    thread_history_str = ""
    # thread_historyが存在するなら
    if thread_history:
        # thread_history でループする
        for message in thread_history["messages"]:
            # ユーザー名を取得
            user_info = client.users_info(user=message["user"])
            user_name = user_info["user"]["name"]
            thread_history_str += user_name + ": " + message["text"] + "\n"

    try:
        gptmessage = gpt35(text, channel, parent_ts, client, thread_history_str)
    except:
        # エラー詳細をprint出力
        import traceback

        traceback.print_exc()
        gptmessage = "エラーが発生しました。"

    say(text=gptmessage, channel=channel, thread_ts=parent_ts)


app.event("app_mention")(
    ack=just_ack,
    lazy=[mention_event_ack],
)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
