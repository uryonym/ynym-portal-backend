class ApplicationController < ActionController::API
  include FirebaseAuthenticator
  before_action :authenticate, if: proc { Rails.env.production? }
  class AuthenticationError < StandardError; end
  rescue_from AuthenticationError, with: :not_authenticated

  def authenticate
    payload = decode(request.headers["Authorization"]&.split&.last)
    puts(payload)
    raise AuthenticationError unless current_user(payload["user_id"])
  end

  def current_user(user_id = nil)
    @current_user ||= User.find_by(uid: user_id)
  end

  private def not_authenticated
    render json: { error: {messages: ["ログインしてください"] } }, status: :unauchorized
  end
end
