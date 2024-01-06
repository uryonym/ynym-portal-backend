class PageSerializer < ActiveModel::Serializer
  attributes :id, :title, :content, :seq
end
