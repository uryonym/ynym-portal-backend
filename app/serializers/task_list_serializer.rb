# frozen_string_literal: true

class TaskListSerializer < ActiveModel::Serializer
  attributes :id, :name, :seq, :uid
end
