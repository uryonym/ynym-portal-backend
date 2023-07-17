class ApplicationController < ActionController::API
  include FirebaseAuthenticator
  include ActionController::HttpAuthentication::Token::ControllerMethods

  before_action :authenticate_token
  class AuthenticationError < StandardError; end
  rescue_from AuthenticationError, with: :not_authenticated

  def authenticate_token
    authenticate_with_http_token do |token, _options|
      payload = decode(token)
      raise AuthenticationError unless current_user(payload["user_id"])
    end
  end

  def current_user(user_id = nil)
    @current_user ||= User.find_by(uid: user_id)
  end

  private def not_authenticated
    render json: { error: {messages: ["ログインしてください"] } }, status: :unauchorized
  end
end
