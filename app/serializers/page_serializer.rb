# frozen_string_literal: true

class PageSerializer < ActiveModel::Serializer
  attributes :id, :title, :content, :seq, :created_at, :updated_at
end
