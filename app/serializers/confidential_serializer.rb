# frozen_string_literal: true

class ConfidentialSerializer < ActiveModel::Serializer
  attributes :id, :service_name, :login_id, :password, :other, :created_at, :updated_at
end
