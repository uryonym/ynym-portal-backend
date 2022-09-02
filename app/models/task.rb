class Task < ApplicationRecord
  belongs_to :user, primary_key: :uid, foreign_key: :uid
end
