# frozen_string_literal: true

class Note < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :seq, presence: true

  # アソシエーション
  belongs_to :user, primary_key: :uid, foreign_key: :uid
  has_many :sections, -> { order(:seq) }
end
