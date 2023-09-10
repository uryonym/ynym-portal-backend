# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: "Star Wars" }, { name: "Lord of the Rings" }])
#   Character.create(name: "Luke", movie: movies.first)

require 'faker'

# 10.times do |n|
#   TaskList.create!(
#     name: Faker::Color.color_name,
#     uid: 'uTnu3ZWTGRUV4gglrxMsYJupoRI3',
#     seq: n
#   )
# end

TaskList.all.each do |task_list|
  15.times do |n|
    Task.create!(
      title: Faker::Restaurant.name,
      description: Faker::Restaurant.description,
      dead_line: Faker::Date.forward,
      is_complete: Faker::Boolean.boolean(true_ratio: 0.3),
      uid: 'uTnu3ZWTGRUV4gglrxMsYJupoRI3',
      task_list_id: task_list.id
    )
  end
end
