class TaskListSerializer < ActiveModel::Serializer
  attributes :id, :name, :seq

  has_many :tasks
end
