class Api::V1::TasksController < ApplicationController
  def index
    tasks = Task.where(uid: @current_user.uid).order(:dead_line, :created_at)
    render json: tasks
  end

  def create
    task = Task.new(task_params)
    task.uid = @current_user.uid
    if task.save
      render json: task
    else
      render json: task.errors, status: :unprocessable_entity
    end
  end

  def show
    task = Task.find(params[:id])
    render json: task
  end

  def update
    task = Task.find(params[:id])
    if task.update(task_params)
      render json: task
    else
      render json: task.errors, status: :unprocessable_entity
    end
  end

  def destroy
    task = Task.find(params[:id])
    task.destroy!
    render json: task
  end

  private def task_params
    params.require(:task).permit(
      :id,
      :title,
      :description,
      :dead_line,
      :is_complete,
      :task_list_id,
      :created_at
    )
  end
end
