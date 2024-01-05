class Page < ApplicationRecord
  # バリデーション
  validates :title, presence: true
  validates :content, presence: true
  validates :uid, presence: true
  validates :seq, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  belongs_to :note
  belongs_to :section
end
