# frozen_string_literal: true

class NoteSerializer < ActiveModel::Serializer
  attributes :id, :name, :seq, :created_at, :updated_at
end
