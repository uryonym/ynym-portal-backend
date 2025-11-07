"""アプリケーション用のカスタム例外クラス."""


class ApplicationException(Exception):
    """アプリケーション用の基本例外クラス."""

    def __init__(self, message: str, status_code: int = 500):
        """例外を初期化.

        Args:
            message: 例外メッセージ
            status_code: HTTP ステータスコード
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """検証に失敗した場合に発生."""

    def __init__(self, message: str):
        """検証例外を初期化."""
        super().__init__(message, status_code=422)


class NotFoundException(ApplicationException):
    """リソースが見つからない場合に発生."""

    def __init__(self, message: str = "リソースが見つかりません"):
        """見つからない例外を初期化."""
        super().__init__(message, status_code=404)


class AuthenticationException(ApplicationException):
    """認証に失敗した場合に発生."""

    def __init__(self, message: str = "認証に失敗しました"):
        """認証例外を初期化."""
        super().__init__(message, status_code=401)


class AuthorizationException(ApplicationException):
    """認可に失敗した場合に発生."""

    def __init__(self, message: str = "アクセス権限が不足しています"):
        """認可例外を初期化."""
        super().__init__(message, status_code=403)
