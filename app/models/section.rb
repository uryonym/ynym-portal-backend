# frozen_string_literal: true

class Section < ApplicationRecord
  # バリデーション
  validates :name, presence: true
  validates :seq, presence: true

  # アソシエーション
  belongs_to :note
  has_many :pages, -> { order(:seq) }
end
