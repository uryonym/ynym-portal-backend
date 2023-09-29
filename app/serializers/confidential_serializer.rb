class ConfidentialSerializer < ActiveModel::Serializer
  attributes :id, :service_name, :login_id, :password, :other, :created_at
end
