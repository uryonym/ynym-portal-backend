# frozen_string_literal: true

class TaskSerializer < ActiveModel::Serializer
  attributes :id,
    :title,
    :description,
    :dead_line,
    :is_complete,
    :created_at,
    :updated_at
end
