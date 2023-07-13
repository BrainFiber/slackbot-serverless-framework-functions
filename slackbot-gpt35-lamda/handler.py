try:
    import unzip_requirements  # type: ignore
except ImportError:
    pass


# これより以降は AWS Lambda 環境で実行したときのみ実行されます

from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from service.slack import app

# ロギングを AWS Lambda 向けに初期化します
SlackRequestHandler.clear_all_log_handlers()


# AWS Lambda 環境で実行される関数
def handler(event, context):
    # AWS Lambda 環境のリクエスト情報を app が処理できるよう変換してくれるアダプター
    slack_handler = SlackRequestHandler(app=app)
    # 応答はそのまま AWS Lambda の戻り値として返せます
    return slack_handler.handle(event, context)
