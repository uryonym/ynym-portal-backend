class User < ApplicationRecord
  has_many :tasks, primary_key: :uid, foreign_key: :uid
end
