class AuthInfo < ApplicationRecord
  # バリデーション
  validates :service_name, presence: true
  validates :login_id, presence: true
end
