# frozen_string_literal: true

require "jwt"

module SupabaseAuthenticator
  ISS_URL = "https://pcwmuaduiowvznblzoqf.supabase.co/auth/v1"

  def decode(token)
    secret = "YTEYxpLtQTbqXqKCAm2lnLrsipgf2O6fbSVwgRHgo2aakajxQtbmaXoBY0NZYlB+WmfWKmKEacfi6GyOGXNDDA=="
    decode_token, _ = JWT.decode(token, secret, true, { iss: ISS_URL })
    decode_token
  end
end
