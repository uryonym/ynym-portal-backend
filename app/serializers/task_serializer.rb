class TaskSerializer < ActiveModel::Serializer
  attributes :id, :title, :description, :dead_line, :is_complete, :created_at
end
