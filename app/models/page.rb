# frozen_string_literal: true

class Page < ApplicationRecord
  # バリデーション
  validates :title, presence: true
  validates :content, presence: true
  validates :seq, presence: true

  # アソシエーション
  belongs_to :section
end
