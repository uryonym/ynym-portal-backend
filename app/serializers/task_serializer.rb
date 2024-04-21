class TaskSerializer < ActiveModel::Serializer
  attributes :id,
             :title,
             :description,
             :dead_line,
             :is_complete,
             :task_list_id,
             :created_at
end
