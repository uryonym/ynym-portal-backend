class Note < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :uid, presence: true
  validates :seq, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  has_many :sections
end
