class Page < ApplicationRecord
  # バリデーション
  validates :title, presence: true
  validates :content, presence: true
  validates :uid, presence: true
  validates :seq, presence: true
  validates :note_id, presence: true
  validates :section_id, presence: true
end
