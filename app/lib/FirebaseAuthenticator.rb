require "jwt"
require "net/http"

module FirebaseAuthenticator
  class InvalidTokenError < StandardError
  end

  ALGORITHM = "RS256".freeze
  ISSUER_URI_BASE = "https://securetoken.google.com/".freeze
  CERTS_URI =
    "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com".freeze
  CERTS_CACHE_KEY = "firebase_auth_certificates"
  PROJECT_ID = "ynym-portal-9a97e"

  def decode(token)
    options = {
      algorithm: ALGORITHM,
      iss: ISSUER_URI_BASE + PROJECT_ID,
      verify_iss: true,
      aud: PROJECT_ID,
      verify_aud: true,
      verify_iat: false
    }

    payload, _ =
      JWT.decode(token, nil, true, options) do |header|
        cert = fetch_certificates[header["kid"]]
        cert.present? ? OpenSSL::X509::Certificate.new(cert).public_key : nil
      end

    unless Time.zone.at(payload["auth_time"]).past?
      raise InvalidTokenError.new("Invalid auth_time")
    end
    raise InvalidTokenError.new("Invalid sub") if payload["sub"].empty?

    payload
  rescue JWT::DecodeError => e
    Rails.logger.error e.message
    Rails.logger.error e.backtrace.join("\n")

    raise InvalidTokenError.new(e.message)
  end

  private

  def fetch_certificates
    cached = Rails.cache.read(CERTS_CACHE_KEY)
    return cached if cached.present?

    res = Net::HTTP.get_response(URI(CERTS_URI))
    raise "Fetch certificates error" unless res.is_a?(Net::HTTPSuccess)

    body = JSON.parse(res.body)
    expires_at = Time.zone.parse(res.header["expires"])
    Rails.cache.write(
      CERTS_CACHE_KEY,
      body,
      expires_in: expires_at - Time.current
    )

    body
  end
end
