# frozen_string_literal: true

require "jwt"

module SupabaseAuthenticator
  ISS_URL = "https://pcwmuaduiowvznblzoqf.supabase.co/auth/v1"

  def decode(token)
    secret = ENV["SUPABASE_JWT_SECRET"]
    decode_token, _ = JWT.decode(token, secret, true, { iss: ISS_URL })
    decode_token
  end
end
