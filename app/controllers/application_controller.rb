# frozen_string_literal: true

class ApplicationController < ActionController::API
  include SupabaseAuthenticator
  before_action :authenticate_token

  class AuthenticationError < StandardError; end
  rescue_from AuthenticationError, with: :not_authenticated

  def authenticate_token
    payload = decode(request.headers["Authorization"]&.split&.last)
    raise AuthenticationError unless payload
    raise AuthenticationError unless current_user(payload["sub"])
  end

  def current_user(user_id = nil)
    @current_user ||= User.find_by(uid: user_id)
  end

  private def not_authenticated
    render(json: { error: { messages: ["ログインしてください"] } }, status: :unauthorized)
  end
end
